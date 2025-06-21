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
            user='adminpi',
            password='Pferd@123',     # ajuste aqui se tiver senha
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
    Cria todas as tabelas necessárias se não existirem e insere dados padrão apenas se não houver usuários.
    """
    conn = create_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cursor:
            # Tabela de usuários
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(50) NOT NULL UNIQUE,
                    senha VARCHAR(100) NOT NULL,
                    nivel INT NOT NULL COMMENT '1=admin, 2=entregador'
                );
            """)

            # Tabela de rotas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rotas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status ENUM('pendente', 'em_andamento', 'concluida') DEFAULT 'pendente'
                );
            """)

            # Tabela de endereços
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS enderecos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    rua VARCHAR(200) NOT NULL,
                    numero VARCHAR(20),
                    bairro VARCHAR(100),
                    cidade VARCHAR(100) NOT NULL,
                    estado VARCHAR(2) NOT NULL,
                    cep VARCHAR(9) NOT NULL,
                    complemento TEXT,
                    latitude DOUBLE,
                    longitude DOUBLE
                );
            """)

            # Tabela de entregas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS entregas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    rota_id INT NOT NULL,
                    endereco_id INT NOT NULL,
                    ordem INT NOT NULL,
                    status ENUM('pendente', 'em_andamento', 'entregue', 'cancelada') DEFAULT 'pendente',
                    data_entrega DATETIME,
                    observacoes TEXT,
                    veiculo_id INT DEFAULT 1,
                    FOREIGN KEY (rota_id) REFERENCES rotas(id),
                    FOREIGN KEY (endereco_id) REFERENCES enderecos(id)
                );
            """)

            # Tabela de veículos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS veiculos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    placa VARCHAR(10) NOT NULL UNIQUE,
                    modelo VARCHAR(50),
                    ano INT,
                    capacidade_kg FLOAT,
                    entregador_id INT,
                    FOREIGN KEY (entregador_id) REFERENCES users(id) ON DELETE SET NULL
                );
            """)

            # Tabela de ligação Rota <-> Veículo (Muitos-para-Muitos)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rota_veiculos (
                    rota_id INT,
                    veiculo_id INT,
                    PRIMARY KEY (rota_id, veiculo_id),
                    FOREIGN KEY (rota_id) REFERENCES rotas(id) ON DELETE CASCADE,
                    FOREIGN KEY (veiculo_id) REFERENCES veiculos(id) ON DELETE CASCADE
                );
            """)

            # Verificar se já existem usuários
            cursor.execute("SELECT COUNT(*) as total FROM users")
            result = cursor.fetchone()
            if result['total'] == 0:
                # Inserir usuários padrão apenas se não houver usuários
                padroes = [
                    ('admin', '123', 1),  # Admin
                    ('entregador', '789', 2),  # Entregador
                ]
                for nome, senha, nivel in padroes:
                    cursor.execute("""
                        INSERT INTO users (nome, senha, nivel)
                        VALUES (%s, %s, %s);
                    """, (nome, senha, nivel))
                logging.info("Usuários padrão inseridos.")
            else:
                logging.info("Usuários já existem, pulando inserção de padrões.")

        conn.commit()
        logging.info("Migração concluída: todas as tabelas foram criadas.")
    except Exception as e:
        logging.error(f"Erro durante a migração: {e}")
        conn.rollback()
    finally:
        conn.close()
