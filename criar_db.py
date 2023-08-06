import sqlite3

if __name__ == '__main__':

    # Ler o código SQL do arquivo
    with open('criar_db.sql', 'r') as file:
        sql_code = file.read()
        
    # Conectar ao banco de dados
    with sqlite3.connect('db.sqlite') as connection:
        cursor = connection.cursor()

        # Executar o código
        cursor.executescript(sql_code)

        # Refletir as mudanças no banco
        connection.commit()

        # Fechar o cursor
        cursor.close()
