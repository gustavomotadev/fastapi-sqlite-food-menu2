import unicodedata

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
    def is_alnum_under(val: str) -> str:
        for c in val:
            if not c.isalnum() and c != '-':
                raise ValueError
        return val
