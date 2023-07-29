from pydantic import BaseModel, Field, validator
from util import Utilidades

class CardapioOut(BaseModel):
    codigo: str = Field(min_length=2, max_length=50)
    nome: str = Field(min_length=2, max_length=50)
    descricao: str = Field(max_length=255)

    @validator('codigo')
    def validar_codigo(codigo: str) -> str:
        return Utilidades.is_alnum_under(codigo)

class CardapioIn(BaseModel):
    nome: str = Field(min_length=2, max_length=50)
    descricao: str = Field(max_length=255)
 
class DescricaoCardapio(BaseModel):
    descricao: str = Field(max_length=255)
 
class ProdutoOut(BaseModel):
    codigo: str = Field(min_length=2, max_length=50)
    codigo_cardapio: str = Field(min_length=2, max_length=50)
    nome: str = Field(min_length=2, max_length=50)
    descricao: str = Field(max_length=255)
    preco: float = Field(ge=0)
    restricao: str = Field(min_length=2, max_length=20)

    @validator('codigo', 'codigo_cardapio')
    def validar_codigo(codigo: str) -> str:
        return Utilidades.is_alnum_under(codigo)

class ProdutoIn(BaseModel):
    codigo_cardapio: str = Field(min_length=2, max_length=50)
    nome: str = Field(min_length=2, max_length=50)
    descricao: str = Field(max_length=255)
    preco: float = Field(ge=0)
    restricao: str = Field(min_length=2, max_length=20)

    @validator('codigo_cardapio')
    def validar_codigo(codigo: str) -> str:
        return Utilidades.is_alnum_under(codigo)
 
class PrecoProduto(BaseModel):
    preco: float = Field(ge=0)