from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from database import create_connection

class HistoryWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Histórico de Rotas Concluídas")
        self.setGeometry(200, 200, 700, 500)
        
        layout = QVBoxLayout(self)
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4) # Nome, Data, Status, Veículos
        self.history_table.setHorizontalHeaderLabels(["Nome da Rota", "Data de Criação", "Status", "Veículos"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.history_table)
        
        self.load_history_data()

    def load_history_data(self):
        """Busca e exibe as rotas concluídas."""
        try:
            conn = create_connection()
            with conn.cursor() as cursor:
                if self.username == 'admin':
                    # Admin vê todas as rotas concluídas
                    query = """
                        SELECT r.nome, r.data_criacao, r.status
                        FROM rotas r
                        WHERE r.status = 'concluida'
                        ORDER BY r.data_criacao DESC
                    """
                    params = []
                else:
                    # Entregadores veem apenas rotas onde são motoristas de algum veículo
                    query = """
                        SELECT DISTINCT r.nome, r.data_criacao, r.status
                        FROM rotas r
                        JOIN rota_veiculos rv ON r.id = rv.rota_id
                        JOIN veiculos v ON rv.veiculo_id = v.id
                        JOIN users u ON v.entregador_id = u.id
                        WHERE r.status = 'concluida'
                        AND u.nome = %s
                        ORDER BY r.data_criacao DESC
                    """
                    params = [self.username]
                
                cursor.execute(query, params)
                routes = cursor.fetchall()

            self.history_table.setRowCount(0)
            for row_num, route in enumerate(routes):
                self.history_table.insertRow(row_num)
                self.history_table.setItem(row_num, 0, QTableWidgetItem(route['nome']))
                data_str = route['data_criacao'].strftime('%d/%m/%Y %H:%M:%S') if route['data_criacao'] else ''
                self.history_table.setItem(row_num, 1, QTableWidgetItem(data_str))
                self.history_table.setItem(row_num, 2, QTableWidgetItem(route['status']))
                
                # Obter veículos da rota
                veiculos_info = self.get_veiculos_rota(route['nome'])
                self.history_table.setItem(row_num, 3, QTableWidgetItem(veiculos_info))

        except Exception as e:
            QMessageBox.critical(self, "Erro de Banco de Dados", f"Não foi possível carregar o histórico: {e}")
        finally:
            if conn: conn.close()

    def get_veiculos_rota(self, rota_nome):
        """Obtém informações dos veículos associados a uma rota pelo nome."""
        conn = create_connection()
        if not conn:
            return "N/A"
        
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT v.placa, u.nome as motorista
                    FROM rotas r
                    JOIN rota_veiculos rv ON r.id = rv.rota_id
                    JOIN veiculos v ON rv.veiculo_id = v.id
                    LEFT JOIN users u ON v.entregador_id = u.id
                    WHERE r.nome = %s
                    ORDER BY v.placa
                """
                cursor.execute(sql, (rota_nome,))
                veiculos = cursor.fetchall()
                
                if not veiculos:
                    return "Nenhum veículo"
                
                # Formatar lista de veículos
                veiculos_info = []
                for veiculo in veiculos:
                    motorista = veiculo['motorista'] or 'N/A'
                    veiculos_info.append(f"{veiculo['placa']} ({motorista})")
                
                return ", ".join(veiculos_info)
                
        except Exception as e:
            print(f"Erro ao obter veículos da rota: {e}")
            return "Erro"
        finally:
            if conn: conn.close() 