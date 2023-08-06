from fastapi import APIRouter, HTTPException, status, Depends
import dtos
from util import Utilidades
from repositorio_cardapio import RepositorioCardapio as RCardapio
from repositorio_produto import RepositorioProduto as RProduto
from dependencias import obter_repo_cardapio, obter_repo_produto

router = APIRouter()

@router.get('/produto/')
async def listar_produtos(codigo_cardapio: str = '', 
    preco_min: int = -1, preco_max: int = 99999, 
    restricao: str = '', 
    repo_cardapio: RCardapio = Depends(obter_repo_cardapio),
    repo_produto: RProduto = Depends(obter_repo_produto)
): 
    if (codigo_cardapio != '' and 
        not repo_cardapio.consultar(codigo_cardapio)):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')
    
    listados = repo_produto.consultar_todos(preco_min, 
        preco_max, codigo_cardapio, restricao)
                
    return listados
 
@router.get('/produto/{codigo_produto}')
async def consultar_produto(codigo_produto: str,
    repo_produto: RProduto = Depends(obter_repo_produto)
): 
    encontrado = repo_produto.consultar(codigo_produto)

    if not encontrado:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Produto não encontrado.')
 
    return encontrado
 
@router.post('/produto/', status_code=status.HTTP_201_CREATED)
async def cadastrar_produto(dto_produto: dtos.ProdutoIn,
    util: Utilidades = Depends(Utilidades),
    repo_cardapio: RCardapio = Depends(obter_repo_cardapio),
    repo_produto: RProduto = Depends(obter_repo_produto)
):
    cardapio = repo_cardapio.consultar(dto_produto.codigo_cardapio)

    if not cardapio:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')
    
    codigo = util.criar_codigo(dto_produto.nome)

    encontrado = repo_produto.consultar(codigo)

    if encontrado:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
            'Produto com código similar já existe.')

    repo_produto.criar(codigo, dto_produto.codigo_cardapio,
        dto_produto.nome, dto_produto.descricao, dto_produto.preco,
        dto_produto.restricao)
    
    return repo_produto.consultar(codigo)
 
@router.put('/produto/{codigo_produto}')
async def alterar_produto(codigo_produto: str, 
    dto_produto: dtos.ProdutoIn,
    repo_cardapio: RCardapio = Depends(obter_repo_cardapio),
    repo_produto: RProduto = Depends(obter_repo_produto)
): 
    encontrado = repo_produto.consultar(codigo_produto)

    if not encontrado:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Produto não encontrado.')
 
    cardapio = repo_cardapio.consultar(dto_produto.codigo_cardapio)

    if not cardapio:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')
 
    repo_produto.alterar(codigo_produto, dto_produto.codigo_cardapio,
        dto_produto.nome, dto_produto.descricao, dto_produto.preco,
        dto_produto.restricao)
    
    return repo_produto.consultar(codigo_produto)
 
@router.delete('/produto/{codigo_produto}')
async def remover_produto(codigo_produto: str,
    repo_produto: RProduto = Depends(obter_repo_produto)
):
    encontrado = repo_produto.consultar(codigo_produto)

    if not encontrado:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Produto não encontrado.')
 
    return encontrado
 
@router.patch('/produto/{codigo_produto}')
async def alterar_preco_produto(codigo_produto: str, 
    preco_produto: dtos.PrecoProduto,
    repo_produto: RProduto = Depends(obter_repo_produto)
):    
    encontrado = repo_produto.consultar(codigo_produto)

    if not encontrado:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Produto não encontrado.')
 
    repo_produto.alterar(codigo_produto, encontrado.codigo_cardapio,
        encontrado.nome, encontrado.descricao, 
        preco_produto.preco, encontrado.restricao)

    return repo_produto.consultar(codigo_produto)
