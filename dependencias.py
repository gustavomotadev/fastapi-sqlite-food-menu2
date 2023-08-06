from repositorio_produto import RepositorioProduto
from repositorio_cardapio import RepositorioCardapio

NOME_DB = 'db.sqlite'

def obter_repo_cardapio():
    return RepositorioCardapio(NOME_DB)

def obter_repo_produto():
    return RepositorioProduto(NOME_DB)