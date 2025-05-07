import mysql.connector

def create_connection():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='rotas',
        )

        if conexao.is_connected():
            print('CONECTADO PAI')

        return conexao  # O return deve estar dentro do try
    except mysql.connector.Error as erro:
        print(f'Erro detectado: {erro}')
        return None  # Caso haja erro, retornamos None para indicar que a conexão falhou
