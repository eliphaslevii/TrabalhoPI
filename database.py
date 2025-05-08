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

        return conexao
    except mysql.connector.Error as erro:
        print(f'Erro detectado: {erro}')
        return None

def migrate_database():
    try:
        connection = create_connection()
        if connection is None:
            return

        cursor = connection.cursor()

        # Cria a tabela 'users' se não existir
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(50) NOT NULL UNIQUE,
                senha VARCHAR(100) NOT NULL
            );
        """)

        connection.commit()
        cursor.close()
        connection.close()
        logging.info("Migração concluída: tabela 'users' verificada/criada.")

    except mysql.connector.Error as err:
        logging.error(f"Erro na migração: {err}")