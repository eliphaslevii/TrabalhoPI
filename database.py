import mysql.connector
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def create_connection():
    """
    Retorna uma conexão com o banco de dados MySQL 'rotas',
    ou None em caso de erro.
    """
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='rotas',
        )
        if conn.is_connected():
            logging.info("Conectado ao banco de dados 'rotas'.")
        return conn
    except mysql.connector.Error as err:
        logging.error(f"Erro de conexão: {err}")
        return None

def migrate_database():
    """
    Cria a tabela 'users' (se não existir) e insere
    os usuários padrão com seus níveis, sem duplicar.
    """
    conn = create_connection()
    if not conn:
        return

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(50) NOT NULL UNIQUE,
            senha VARCHAR(100) NOT NULL,
            nivel INT NOT NULL
        );
    """)

    # Insere somente se não existir
    padroes = [
        ('admin',       '123', 1),
        ('gestor',      '456', 2),
        ('entregador',  '789', 3),
    ]
    for nome, senha, nivel in padroes:
        cursor.execute("""
            INSERT INTO users (nome, senha, nivel)
            SELECT %s, %s, %s
            WHERE NOT EXISTS (
                SELECT 1 FROM users WHERE nome = %s
            );
        """, (nome, senha, nivel, nome))

    conn.commit()
    cursor.close()
    conn.close()
    logging.info("Migração concluída: tabela 'users' pronta e usuários padrão inseridos.")
