from fastapi import APIRouter, HTTPException, status, Depends
import db
import dtos
from util import Utilidades

router = APIRouter()

@router.get('/produto/')
async def listar_produtos(codigo_cardapio: str = '', preco_min: int = -1, 
    preco_max: int = 99999, restricao: str = ''):
 
    if codigo_cardapio != '' and codigo_cardapio not in db.banco_cardapios:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')
    
    listados = []

    for produto in db.banco_produtos.values():

        if (produto['preco'] >= preco_min and produto['preco'] <= preco_max
            and (restricao == '' or produto['restricao'] == restricao)
            and (codigo_cardapio == '' or 
                 produto['codigo_cardapio'] == codigo_cardapio)):
                
                listados.append(produto)
                
    return listados
 
@router.get('/produto/{codigo_produto}')
async def consultar_produto(codigo_produto: str):
 
    if codigo_produto not in db.banco_produtos:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Produto não encontrado.')
 
    return db.banco_produtos[codigo_produto]
 
@router.post('/produto/', status_code=status.HTTP_201_CREATED)
async def cadastrar_produto(produto: dtos.ProdutoIn,
    util: Utilidades = Depends(Utilidades)):
 
    if produto.codigo_cardapio not in db.banco_cardapios:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')
    
    codigo = util.criar_codigo(produto.nome)
    db.banco_produtos[codigo] = produto.model_dump()
    db.banco_produtos[codigo]['codigo'] = codigo
    return db.banco_produtos[codigo]
 
@router.put('/produto/{codigo_produto}')
async def alterar_produto(codigo_produto: str, produto: dtos.ProdutoIn):
 
    if codigo_produto not in db.banco_produtos:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Produto não encontrado.')
 
    if produto.codigo_cardapio not in db.banco_cardapios:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')
 
    db.banco_produtos[codigo_produto] = produto.model_dump()
    db.banco_produtos[codigo_produto]['codigo'] = codigo_produto
    return db.banco_produtos[codigo_produto]
 
@router.delete('/produto/{codigo_produto}')
async def remover_produto(codigo_produto: str):
    
    if codigo_produto not in db.banco_produtos:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Produto não encontrado.')
 
    return db.banco_produtos.pop(codigo_produto)
 
@router.patch('/produto/{codigo_produto}')
async def alterar_preco_produto(codigo_produto: str, 
    preco_produto: dtos.PrecoProduto):
    
    if codigo_produto not in db.banco_produtos:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Produto não encontrado.')
 
    db.banco_produtos[codigo_produto]['preco'] = preco_produto.preco
    return db.banco_produtos[codigo_produto]
