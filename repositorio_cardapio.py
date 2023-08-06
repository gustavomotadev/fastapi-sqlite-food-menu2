import sqlite3
from typing import List
from dtos import CardapioOut

class RepositorioCardapio:
        
    FOREIGN_KEY_SQLITE = 'PRAGMA foreign_keys=ON;'
    LINHAS_AFETADAS_SQLITE = 'SELECT changes();'

    @staticmethod
    def montar(tupla_dados: tuple) -> CardapioOut:
        codigo, nome, descricao = tupla_dados
        return CardapioOut(codigo=codigo, nome=nome, 
            descricao=descricao)

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
    
    def criar(self, codigo: str, nome: str, descricao: str) -> int:
        query = 'INSERT OR IGNORE INTO cardapio (codigo, nome, descricao) VALUES (?, ?, ?);'
        self.abrir_conexao()
        self.cursor.execute(query, (codigo, nome, descricao))
        self.connection.commit()
        return self.obter_mudancas_fechar()
    
    def consultar(self, codigo: str) -> CardapioOut:
        query = 'SELECT codigo,nome,descricao FROM cardapio WHERE codigo = ?;'
        self.abrir_conexao()
        self.cursor.execute(query, (codigo,))
        cardapio = self.cursor.fetchone()
        self.fechar_conexao()
        return self.montar(cardapio) if cardapio else None
    
    def consultar_todos(self) -> List[CardapioOut]:
        query = 'SELECT codigo,nome,descricao FROM cardapio;'
        self.abrir_conexao()
        self.cursor.execute(query)
        cardapios = self.cursor.fetchall()
        self.fechar_conexao()
        return [self.montar(cardapio) for cardapio in cardapios]
    
    def alterar(self, codigo: str, nome: str, descricao: str) -> int:
        query = 'UPDATE cardapio SET nome = ?, descricao = ? WHERE codigo = ?'
        self.abrir_conexao()
        self.cursor.execute(query, (nome, descricao, codigo))
        self.connection.commit()
        return self.obter_mudancas_fechar()
    
    def remover(self, codigo: str) -> int:
        query = 'DELETE FROM cardapio WHERE codigo = ?'
        self.abrir_conexao()
        self.cursor.execute(query, (codigo,))
        self.connection.commit()
        return self.obter_mudancas_fechar()
