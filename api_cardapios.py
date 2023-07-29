from fastapi import APIRouter, HTTPException, status, Depends
import db
import dtos
from util import Utilidades

router = APIRouter()

@router.get('/cardapio/')
async def listar_cardapios():
 
    return list(db.banco_cardapios.values())
 
@router.get('/cardapio/{codigo_cardapio}')
async def consultar_cardapio(codigo_cardapio: str):
 
    if codigo_cardapio not in db.banco_cardapios:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')
 
    return db.banco_cardapios[codigo_cardapio]
 
@router.post('/cardapio/', status_code=status.HTTP_201_CREATED)
async def cadastrar_cardapio(cardapio: dtos.CardapioIn,
    util: Utilidades = Depends(Utilidades)):
 
    codigo = util.criar_codigo(cardapio.nome)
 
    if codigo in db.banco_cardapios:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
            'Código já existe.')
 
    db.banco_cardapios[codigo] = cardapio.model_dump()
    db.banco_cardapios[codigo]['codigo'] = codigo
    return db.banco_cardapios[codigo]
 
@router.put('/cardapio/{codigo_cardapio}')
async def alterar_cardapio(codigo_cardapio: str, cardapio: dtos.CardapioIn):
 
    if codigo_cardapio not in db.banco_cardapios:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')
 
    db.banco_cardapios[codigo_cardapio] = cardapio.model_dump() 
    db.banco_cardapios[codigo_cardapio]['codigo'] = codigo_cardapio
    return db.banco_cardapios[codigo_cardapio]
 
@router.delete('/cardapio/{codigo_cardapio}')
async def remover_cardapio(codigo_cardapio: str):
 
    if codigo_cardapio not in db.banco_cardapios:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')
    
    for produto in db.banco_produtos.items():
        if produto['codigo_cardapio'] == codigo_cardapio:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,
            'Não é possível deletar. Cardápio possui produtos.')
 
    return db.banco_cardapios.pop(codigo_cardapio)
 
@router.patch('/cardapio/{codigo_cardapio}')
async def alterar_descricao_cardapio(codigo_cardapio: str, 
    descricao: dtos.DescricaoCardapio):
 
    if codigo_cardapio not in db.banco_cardapios:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')
 
    db.banco_cardapios[codigo_cardapio]['descricao'] = descricao.descricao
    return db.banco_cardapios[codigo_cardapio]
