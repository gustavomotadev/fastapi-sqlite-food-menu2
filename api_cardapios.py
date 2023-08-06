from fastapi import APIRouter, HTTPException, status, Depends
import dtos
from util import Utilidades
from repositorio_cardapio import RepositorioCardapio as RCardapio
from repositorio_produto import RepositorioProduto as RProduto
from dependencias import obter_repo_cardapio, obter_repo_produto

router = APIRouter()

@router.get('/cardapio/')
async def listar_cardapios(
    repo_cardapio: RCardapio = Depends(obter_repo_cardapio)
):
    return repo_cardapio.consultar_todos()
 
@router.get('/cardapio/{codigo_cardapio}')
async def consultar_cardapio(codigo_cardapio: str,
    repo_cardapio: RCardapio = Depends(obter_repo_cardapio)
):
    encontrado = repo_cardapio.consultar(codigo_cardapio)

    if not encontrado:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')
 
    return encontrado
 
@router.post('/cardapio/', status_code=status.HTTP_201_CREATED)
async def cadastrar_cardapio(dto_cardapio: dtos.CardapioIn,
    util: Utilidades = Depends(Utilidades),
    repo_cardapio: RCardapio = Depends(obter_repo_cardapio)
):
    codigo = util.criar_codigo(dto_cardapio.nome)
 
    if repo_cardapio.consultar(codigo):
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
            'Cardápio com código similar já existe.')
 
    repo_cardapio.criar(codigo, dto_cardapio.nome,
        dto_cardapio.descricao)
    
    return repo_cardapio.consultar(codigo)
 
@router.put('/cardapio/{codigo_cardapio}')
async def alterar_cardapio(codigo_cardapio: str, 
    dto_cardapio: dtos.CardapioIn,
    repo_cardapio: RCardapio = Depends(obter_repo_cardapio)
): 
    encontrado = repo_cardapio.consultar(codigo_cardapio)

    if not encontrado:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')
 
    repo_cardapio.alterar(codigo_cardapio, dto_cardapio.nome,
        dto_cardapio.descricao)
    
    return repo_cardapio.consultar(codigo_cardapio)
 
@router.delete('/cardapio/{codigo_cardapio}')
async def remover_cardapio(codigo_cardapio: str,
    repo_cardapio: RCardapio = Depends(obter_repo_cardapio),
    repo_produto: RProduto = Depends(obter_repo_produto)
): 
    encontrado = repo_cardapio.consultar(codigo_cardapio)

    if not encontrado:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')
    
    if repo_produto.consultar_todos(codigo_cardapio=codigo_cardapio):
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
        'Não é possível deletar. Cardápio possui produtos.')
 
    repo_cardapio.remover(codigo_cardapio)

    return encontrado
 
@router.patch('/cardapio/{codigo_cardapio}')
async def alterar_descricao_cardapio(codigo_cardapio: str, 
    descricao_cardapio: dtos.DescricaoCardapio,
    repo_cardapio: RCardapio = Depends(obter_repo_cardapio)
): 
    encontrado = repo_cardapio.consultar(codigo_cardapio)

    if not encontrado:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')
 
    repo_cardapio.alterar(codigo_cardapio,
        encontrado.nome, descricao_cardapio.descricao)
    
    return repo_cardapio.consultar(codigo_cardapio)
