#!/usr/bin/env python3
"""
Script de migração para atualizar o banco de dados para a nova estrutura.
Remove as colunas antigas e garante a integridade dos dados.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import create_connection
from PyQt5.QtWidgets import QMessageBox, QApplication

def migrate_database():
    """Executa a migração do banco de dados para a nova estrutura."""
    app = QApplication(sys.argv)
    
    conn = create_connection()
    if not conn:
        QMessageBox.critical(None, "Erro", "Não foi possível conectar ao banco de dados.")
        return False

    try:
        with conn.cursor() as cursor:
            print("Iniciando migração do banco de dados...")
            
            # 1. Verificar se as colunas antigas existem
            cursor.execute("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'rotas' 
                AND COLUMN_NAME IN ('entregador_id', 'numero_veiculos')
            """)
            existing_columns = [row['COLUMN_NAME'] for row in cursor.fetchall()]
            
            if existing_columns:
                print(f"Colunas antigas encontradas: {existing_columns}")
                
                # 2. Verificar se a tabela rota_veiculos existe
                cursor.execute("""
                    SELECT COUNT(*) as count 
                    FROM information_schema.tables 
                    WHERE table_schema = DATABASE() 
                    AND table_name = 'rota_veiculos'
                """)
                table_exists = cursor.fetchone()['count'] > 0
                
                if not table_exists:
                    print("Criando tabela rota_veiculos...")
                    cursor.execute("""
                        CREATE TABLE rota_veiculos (
                            rota_id INT,
                            veiculo_id INT,
                            PRIMARY KEY (rota_id, veiculo_id),
                            FOREIGN KEY (rota_id) REFERENCES rotas(id) ON DELETE CASCADE,
                            FOREIGN KEY (veiculo_id) REFERENCES veiculos(id) ON DELETE CASCADE
                        );
                    """)
                
                # 3. Migrar dados existentes se necessário
                if 'entregador_id' in existing_columns:
                    print("Migrando dados de entregador_id...")
                    
                    # Verificar se há rotas com entregador_id preenchido
                    cursor.execute("SELECT COUNT(*) as count FROM rotas WHERE entregador_id IS NOT NULL")
                    rotas_com_entregador = cursor.fetchone()['count']
                    
                    if rotas_com_entregador > 0:
                        print(f"Encontradas {rotas_com_entregador} rotas com entregador_id")
                        
                        # Para cada rota com entregador, criar associação com veículos desse entregador
                        cursor.execute("""
                            SELECT r.id, r.entregador_id, v.id as veiculo_id
                            FROM rotas r
                            JOIN veiculos v ON r.entregador_id = v.entregador_id
                            WHERE r.entregador_id IS NOT NULL
                        """)
                        
                        associacoes = cursor.fetchall()
                        for associacao in associacoes:
                            try:
                                cursor.execute("""
                                    INSERT IGNORE INTO rota_veiculos (rota_id, veiculo_id) 
                                    VALUES (%s, %s)
                                """, (associacao['id'], associacao['veiculo_id']))
                            except Exception as e:
                                print(f"Erro ao associar rota {associacao['id']} com veículo {associacao['veiculo_id']}: {e}")
                
                # 4. Remover colunas antigas
                print("Removendo colunas antigas...")
                for column in existing_columns:
                    try:
                        cursor.execute(f"ALTER TABLE rotas DROP COLUMN {column}")
                        print(f"Coluna {column} removida com sucesso")
                    except Exception as e:
                        print(f"Erro ao remover coluna {column}: {e}")
            
            else:
                print("Nenhuma coluna antiga encontrada. Banco já está atualizado.")
            
            # 5. Verificar se a coluna veiculo_id existe na tabela entregas
            cursor.execute("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'entregas' 
                AND COLUMN_NAME = 'veiculo_id'
            """)
            
            if not cursor.fetchall():
                print("Adicionando coluna veiculo_id à tabela entregas...")
                cursor.execute("""
                    ALTER TABLE entregas 
                    ADD COLUMN veiculo_id INT DEFAULT NULL,
                    ADD FOREIGN KEY (veiculo_id) REFERENCES veiculos(id) ON DELETE SET NULL
                """)
                print("Coluna veiculo_id adicionada com sucesso")
            
            # 6. Adicionar a coluna 'problema' na tabela 'rotas'
            cursor.execute("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'rotas' 
                AND COLUMN_NAME = 'problema'
            """)
            if not cursor.fetchall():
                print("Adicionando coluna 'problema' à tabela 'rotas'...")
                cursor.execute("ALTER TABLE rotas ADD COLUMN problema BOOLEAN DEFAULT FALSE")
                print("Coluna 'problema' adicionada com sucesso.")

            conn.commit()
            print("Migração concluída com sucesso!")
            QMessageBox.information(None, "Sucesso", "Migração do banco de dados concluída com sucesso!")
            return True
            
    except Exception as e:
        conn.rollback()
        error_msg = f"Erro durante a migração: {e}"
        print(error_msg)
        QMessageBox.critical(None, "Erro", error_msg)
        return False
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    migrate_database() 