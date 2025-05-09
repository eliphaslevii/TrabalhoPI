# database.py

import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def create_connection():
    """
    Retorna uma conexão PyMySQL com o banco de dados 'rotas' via TCP,
    ou None em caso de erro.
    """
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='',     # ajuste aqui se tiver senha
            database='rotas',
            cursorclass=pymysql.cursors.DictCursor  # retorna dicts em vez de tuples
        )
        logging.info(f"Conectado ao MySQL via PyMySQL (127.0.0.1:3306), versão {pymysql.__version__}")
        return conn
    except Exception as err:
        logging.error(f"Erro de conexão PyMySQL: {err}")
        return None

def migrate_database():
    """
    Cria a tabela 'users' se necessário e insere usuários-padrão.
    """
    conn = create_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(50) NOT NULL UNIQUE,
                    senha VARCHAR(100) NOT NULL,
                    nivel INT NOT NULL
                );
            """)
            padroes = [
                ('admin', '123', 1),
                ('gestor', '456', 2),
                ('entregador', '789', 3),
            ]
            for nome, senha, nivel in padroes:
                cursor.execute("""
                    INSERT IGNORE INTO users (nome, senha, nivel)
                    VALUES (%s, %s, %s);
                """, (nome, senha, nivel))
        conn.commit()
        logging.info("Migração concluída: tabela 'users' pronta e usuários padrão inseridos.")
    finally:
        conn.close()
