import sqlite3
from typing import Any, List
from dtos import ProdutoOut

class RepositorioProduto:

    FOREIGN_KEY_SQLITE = 'PRAGMA foreign_keys=ON;'
    LINHAS_AFETADAS_SQLITE = 'SELECT changes();'

    @staticmethod
    def montar(tupla_dados: tuple) -> ProdutoOut:
        codigo, codigo_cardapio, nome, descricao, preco, restricao = tupla_dados
        preco = float(preco)
        return ProdutoOut(codigo=codigo, codigo_cardapio=codigo_cardapio, 
            nome=nome, descricao=descricao, preco=preco, restricao=restricao)
        
    def __init__(self, nome_db: str) -> None:
        self.nome_db = nome_db
        self.connection = None
        self.cursor = None
        
    def abrir_conexao(self) -> None:
        self.connection = sqlite3.connect(self.nome_db)
        self.cursor = self.connection.cursor()
        self.ativar_foreign_key()
        
    def fechar_conexao(self) -> None:
        self.cursor.close()
        self.connection.close()
        self.connection = None
        self.cursor = None

    def ativar_foreign_key(self) -> None:
        self.cursor.execute(self.FOREIGN_KEY_SQLITE)

    def obter_mudancas(self) -> int:
        mudancas = self.cursor.execute(self.LINHAS_AFETADAS_SQLITE)
        return mudancas.fetchone()[0]
    
    def obter_mudancas_fechar(self) -> int:
        mudancas = self.obter_mudancas()
        self.fechar_conexao()
        return mudancas
    
    def criar(self, codigo: str, codigo_cardapio: str, 
        nome: str, descricao: str, preco: float, restricao: str) -> int:
        query = 'INSERT OR IGNORE INTO produto (codigo, codigo_cardapio, nome, descricao, preco, restricao) VALUES (?, ?, ?, ?, ?, ?);'
        self.abrir_conexao()
        self.cursor.execute(query, (codigo, codigo_cardapio, nome, descricao, preco, restricao))
        self.connection.commit()
        return self.obter_mudancas_fechar()
    
    def consultar(self, codigo: str) -> ProdutoOut:
        query = 'SELECT codigo,codigo_cardapio,nome,descricao,preco,restricao FROM produto WHERE codigo = ?;'
        self.abrir_conexao()
        self.cursor.execute(query, (codigo,))
        produto = self.cursor.fetchone()
        self.fechar_conexao()
        return self.montar(produto) if produto else produto
    
    def consultar_todos(self, preco_min: int = -1, preco_max: int = 99999, 
            codigo_cardapio: str = '', restricao: str = '') -> List[ProdutoOut]:
        
        query = 'SELECT codigo,codigo_cardapio,nome,descricao,preco,restricao FROM produto WHERE preco >= ? AND preco <= ?'

        parametros = [preco_min, preco_max]

        if codigo_cardapio:
            query += ' AND codigo_cardapio = ?'
            parametros.append(codigo_cardapio)

        if restricao:
            query += ' AND restricao = ?'
            parametros.append(restricao)

        query += ';'
        
        self.abrir_conexao()
        self.cursor.execute(query, tuple(parametros))
        produtos = self.cursor.fetchall()
        self.fechar_conexao()
        return [self.montar(produto) for produto in produtos]
    
    def alterar(self, codigo: str, codigo_cardapio: str, 
        nome: str, descricao: str, preco: float, restricao: str) -> int:
        query = 'UPDATE produto SET codigo_cardapio = ?, nome = ?, descricao = ?, preco = ?, restricao = ? WHERE codigo = ?'
        self.abrir_conexao()
        self.cursor.execute(query, (codigo_cardapio, nome, descricao, preco, restricao, codigo))
        self.connection.commit()
        return self.obter_mudancas_fechar()
    
    def remover(self, codigo: str) -> int:
        query = 'DELETE FROM produto WHERE codigo = ?'
        self.abrir_conexao()
        self.cursor.execute(query, (codigo,))
        self.connection.commit()
        return self.obter_mudancas_fechar()
