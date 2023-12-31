import dtos
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from dependencias import dependencia_token, obter_autenticador
from autenticacao import Autenticador
from repositorio_usuario import RepositorioUsuario as RUsuario
from dependencias import obter_repo_usuario
from util import Utilidades

async def obter_usuario_logado(
    token: str = Depends(dependencia_token),
    aut: Autenticador = Depends(obter_autenticador)
) -> dtos.Usuario:

    dados = aut.validar_token_jwt(token)

    if not dados:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar o token.",
        headers={"WWW-Authenticate": "Bearer"})
    
    return dtos.Usuario(
        nome_usuario=dados.get('nome_usuario'), 
        nome_completo=dados.get('nome_completo'), 
        cargo=dados.get('cargo'))

router = APIRouter()

@router.post('/autenticacao/cadastro', 
    status_code=status.HTTP_201_CREATED)
async def cadastro(cadastro: dtos.Cadastro,
    aut: Autenticador = Depends(obter_autenticador),
    repo_usuario: RUsuario = Depends(obter_repo_usuario),
    util: Utilidades = Depends(Utilidades)
) -> dtos.Usuario:
    
    username = util.criar_codigo(
        cadastro.nome_completo).replace('-', '.')

    if repo_usuario.consultar(username):
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
            'Nome de usuário já existe.')

    salt_senha = aut.gerar_salt()
    hash_senha = aut.gerar_hash_senha(salt_senha,
        cadastro.senha.get_secret_value())

    criado = repo_usuario.criar(username, 
        cadastro.nome_completo, cadastro.cargo, 
        salt_senha, hash_senha)
    
    if not criado:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
            'Não foi possível criar usuário.')
    
    return repo_usuario.consultar(username)

@router.post('/autenticacao/login')
async def login(
    dados_formulario: OAuth2PasswordRequestForm = Depends(),
    aut: Autenticador = Depends(obter_autenticador),
    repo_usuario: RUsuario = Depends(obter_repo_usuario)
) -> dtos.BearerToken:

    salt_usuario = repo_usuario.consultar_salt(
        dados_formulario.username)

    if not salt_usuario:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
            'Credenciais inválidas.')
    
    hash_senha = aut.gerar_hash_senha(salt_usuario,
        dados_formulario.password)
    usuario = repo_usuario.consultar_credenciais(
        dados_formulario.username, salt_usuario, hash_senha)
    
    if not usuario:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
            'Credenciais inválidas.')
    
    token = aut.gerar_token_jwt(usuario.model_dump())
    
    return dtos.BearerToken(access_token=token)

@router.get('/autenticacao/usuario')
async def usuario(
    usuario_logado: dtos.Usuario = Depends(obter_usuario_logado)
) -> dtos.Usuario:

    return usuario_logado

@router.get('/autenticacao/confirmar', 
    dependencies=[Depends(obter_usuario_logado)])
async def usuario() -> None:

    return Response(status_code=status.HTTP_200_OK)