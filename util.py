import unicodedata
from pydantic import SecretStr

class Utilidades:
    @staticmethod
    def criar_codigo(nome: str) -> str:
        # Converter para minúsculas
        nome = nome.lower()
        
        # Remover acentos
        nome = ''.join(c for c in unicodedata.normalize('NFKD', nome) 
            if unicodedata.category(c) != 'Mn')
        
        # Remover todos os caracteres que não são letras, números ou espaços
        nome = ''.join(c for c in nome 
            if c.isascii() and (c.isalnum() or c == ' '))
        
        # Trocar espaços por traços
        nome = nome.replace(' ', '-')
 
        return nome   
    
    @staticmethod
    def is_alnum_hyphen(texto: str) -> str:
        for c in texto:
            if not c.isalnum() and c != '-':
                raise ValueError
        return texto
    
    @staticmethod
    def is_alpha_dot(texto: str) -> str:
        for c in texto:
            if not c.isalpha() and c != '.':
                raise ValueError
        return texto
    
    @staticmethod
    def is_alpha_space(texto: str) -> str:
        for c in texto:
            if not c.isalpha() and c != ' ':
                raise ValueError
        return texto
        
    @staticmethod
    def is_alnum_space(texto: str) -> str:
        for c in texto:
            if not c.isalnum() and c != ' ':
                raise ValueError
        return texto

    @staticmethod
    def validar_senha(senha: SecretStr) -> SecretStr:
        for c in senha.get_secret_value():
            if not c.isalnum() and c not in '._?!@#$%&-+*=':
                raise ValueError
        return senha