from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QPushButton, QTableWidget, 
    QTableWidgetItem, QMessageBox, QHeaderView, QHBoxLayout, QDialog
)
from database import create_connection
from .vehicle_form import VehicleForm # Importar o formulário
from .driver_form import DriverForm # Importar formulário do entregador

class ManagementWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciamento")
        self.setGeometry(150, 150, 800, 500)
        
        # Layout principal
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Abas
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Criar as abas
        self.create_drivers_tab()
        self.create_vehicles_tab()
        
        # Carregar dados iniciais
        self.load_drivers_data()
        self.load_vehicles_data()

    def create_drivers_tab(self):
        """Cria a aba para gerenciamento de entregadores."""
        drivers_tab = QWidget()
        layout = QVBoxLayout(drivers_tab)
        
        # Tabela de entregadores
        self.drivers_table = QTableWidget()
        self.drivers_table.setColumnCount(3) # ID, Nome, Veículo
        self.drivers_table.setHorizontalHeaderLabels(["ID", "Nome", "Veículo Atribuído"])
        self.drivers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.drivers_table)
        
        # Botões de ação
        buttons_layout = QHBoxLayout()
        add_driver_btn = QPushButton("Adicionar Entregador")
        add_driver_btn.clicked.connect(self.add_driver) # Conectado
        buttons_layout.addWidget(add_driver_btn)
        
        remove_driver_btn = QPushButton("Remover Selecionado(s)")
        remove_driver_btn.clicked.connect(self.remove_driver) # Conectado
        buttons_layout.addWidget(remove_driver_btn)
        layout.addLayout(buttons_layout)
        
        self.tabs.addTab(drivers_tab, "Entregadores")

    def create_vehicles_tab(self):
        """Cria a aba para gerenciamento de veículos."""
        vehicles_tab = QWidget()
        layout = QVBoxLayout(vehicles_tab)
        
        # Tabela de veículos
        self.vehicles_table = QTableWidget()
        self.vehicles_table.setColumnCount(5) # ID, Placa, Modelo, Ano, Entregador
        self.vehicles_table.setHorizontalHeaderLabels(["ID", "Placa", "Modelo", "Ano", "Entregador"])
        self.vehicles_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.vehicles_table)
        
        # Botões de ação
        buttons_layout = QHBoxLayout()
        add_vehicle_btn = QPushButton("Adicionar Veículo")
        add_vehicle_btn.clicked.connect(self.add_vehicle) # Conectado
        buttons_layout.addWidget(add_vehicle_btn)
        
        edit_vehicle_btn = QPushButton("Editar Selecionado")
        edit_vehicle_btn.clicked.connect(self.edit_vehicle) # Conectado
        buttons_layout.addWidget(edit_vehicle_btn)

        remove_vehicle_btn = QPushButton("Remover Selecionado(s)")
        remove_vehicle_btn.clicked.connect(self.remove_vehicle) # Conectado
        buttons_layout.addWidget(remove_vehicle_btn)
        layout.addLayout(buttons_layout)

        self.tabs.addTab(vehicles_tab, "Veículos")

    def refresh_data(self):
        """Atualiza os dados de ambas as tabelas."""
        self.load_drivers_data()
        self.load_vehicles_data()

    def add_driver(self):
        """Abre o formulário para adicionar um novo entregador."""
        form = DriverForm()
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            if not data['nome'] or not data['senha']:
                QMessageBox.warning(self, "Entrada Inválida", "Nome e senha são obrigatórios.")
                return

            try:
                conn = create_connection()
                with conn.cursor() as cursor:
                    # O nível 2 é para entregador
                    sql = "INSERT INTO users (nome, senha, nivel) VALUES (%s, %s, 2)"
                    cursor.execute(sql, (data['nome'], data['senha']))
                conn.commit()
                self.refresh_data()
                QMessageBox.information(self, "Sucesso", "Entregador adicionado com sucesso!")
            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Erro de Banco de Dados", f"Falha ao adicionar entregador: {e}")
            finally:
                if conn: conn.close()

    def remove_driver(self):
        """Remove o entregador selecionado."""
        selected_row = self.drivers_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Nenhuma Seleção", "Por favor, selecione um entregador para remover.")
            return

        driver_id = int(self.drivers_table.item(selected_row, 0).text())
        driver_name = self.drivers_table.item(selected_row, 1).text()
        
        reply = QMessageBox.question(self, 'Confirmar Remoção', 
                                     f"Tem certeza que deseja remover o entregador {driver_name}?\n"
                                     f"Qualquer veículo vinculado a ele ficará como 'Não atribuído'.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                conn = create_connection()
                with conn.cursor() as cursor:
                    # Graças ao 'ON DELETE SET NULL', a tabela de veículos será atualizada automaticamente
                    cursor.execute("DELETE FROM users WHERE id = %s", (driver_id,))
                conn.commit()
                self.refresh_data()
                QMessageBox.information(self, "Sucesso", "Entregador removido com sucesso!")
            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Erro de Banco de Dados", f"Falha ao remover entregador: {e}")
            finally:
                if conn: conn.close()

    def add_vehicle(self):
        """Abre o formulário para adicionar um novo veículo."""
        form = VehicleForm()
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            if not data['placa']:
                QMessageBox.warning(self, "Entrada Inválida", "A placa é obrigatória.")
                return
            
            try:
                conn = create_connection()
                with conn.cursor() as cursor:
                    sql = "INSERT INTO veiculos (placa, modelo, ano, entregador_id) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (data['placa'], data['modelo'], data['ano'], data['entregador_id']))
                conn.commit()
                self.refresh_data()
            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Erro de Banco de Dados", f"Falha ao adicionar veículo: {e}")
            finally:
                if conn: conn.close()
    
    def edit_vehicle(self):
        """Abre o formulário para editar o veículo selecionado."""
        selected_row = self.vehicles_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Nenhuma Seleção", "Por favor, selecione um veículo para editar.")
            return
            
        vehicle_id = int(self.vehicles_table.item(selected_row, 0).text())
        form = VehicleForm(vehicle_id=vehicle_id)
        
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            if not data['placa']:
                QMessageBox.warning(self, "Entrada Inválida", "A placa é obrigatória.")
                return

            try:
                conn = create_connection()
                with conn.cursor() as cursor:
                    sql = """
                        UPDATE veiculos 
                        SET placa = %s, modelo = %s, ano = %s, entregador_id = %s
                        WHERE id = %s
                    """
                    cursor.execute(sql, (data['placa'], data['modelo'], data['ano'], data['entregador_id'], vehicle_id))
                conn.commit()
                self.refresh_data()
            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Erro de Banco de Dados", f"Falha ao editar veículo: {e}")
            finally:
                if conn: conn.close()

    def remove_vehicle(self):
        """Remove o veículo selecionado."""
        selected_row = self.vehicles_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Nenhuma Seleção", "Por favor, selecione um veículo para remover.")
            return

        vehicle_id = int(self.vehicles_table.item(selected_row, 0).text())
        placa = self.vehicles_table.item(selected_row, 1).text()
        
        reply = QMessageBox.question(self, 'Confirmar Remoção', 
                                     f"Tem certeza que deseja remover o veículo de placa {placa}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                conn = create_connection()
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM veiculos WHERE id = %s", (vehicle_id,))
                conn.commit()
                self.refresh_data()
            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Erro de Banco de Dados", f"Falha ao remover veículo: {e}")
            finally:
                if conn: conn.close()

    def load_drivers_data(self):
        """Busca e exibe os dados dos entregadores na tabela."""
        try:
            conn = create_connection()
            with conn.cursor() as cursor:
                # Usamos um LEFT JOIN para ver o veículo mesmo que não haja um
                sql = """
                    SELECT u.id, u.nome, v.placa 
                    FROM users u
                    LEFT JOIN veiculos v ON u.id = v.entregador_id
                    WHERE u.nivel = 2
                    ORDER BY u.nome;
                """
                cursor.execute(sql)
                drivers = cursor.fetchall()
            
            self.drivers_table.setRowCount(0)
            for row_num, driver in enumerate(drivers):
                self.drivers_table.insertRow(row_num)
                self.drivers_table.setItem(row_num, 0, QTableWidgetItem(str(driver['id'])))
                self.drivers_table.setItem(row_num, 1, QTableWidgetItem(driver['nome']))
                placa = driver['placa'] if driver['placa'] else "Nenhum"
                self.drivers_table.setItem(row_num, 2, QTableWidgetItem(placa))
        except Exception as e:
            QMessageBox.critical(self, "Erro de Banco de Dados", f"Não foi possível carregar os entregadores: {e}")
        finally:
            if conn: conn.close()

    def load_vehicles_data(self):
        """Busca e exibe os dados dos veículos na tabela."""
        try:
            conn = create_connection()
            with conn.cursor() as cursor:
                # LEFT JOIN para mostrar o nome do entregador
                sql = """
                    SELECT v.id, v.placa, v.modelo, v.ano, u.nome as entregador_nome
                    FROM veiculos v
                    LEFT JOIN users u ON v.entregador_id = u.id
                    ORDER BY v.placa;
                """
                cursor.execute(sql)
                vehicles = cursor.fetchall()

            self.vehicles_table.setRowCount(0)
            for row_num, vehicle in enumerate(vehicles):
                self.vehicles_table.insertRow(row_num)
                self.vehicles_table.setItem(row_num, 0, QTableWidgetItem(str(vehicle['id'])))
                self.vehicles_table.setItem(row_num, 1, QTableWidgetItem(vehicle['placa']))
                self.vehicles_table.setItem(row_num, 2, QTableWidgetItem(vehicle['modelo']))
                self.vehicles_table.setItem(row_num, 3, QTableWidgetItem(str(vehicle['ano'])))
                entregador = vehicle['entregador_nome'] if vehicle['entregador_nome'] else "Não atribuído"
                self.vehicles_table.setItem(row_num, 4, QTableWidgetItem(entregador))
        except Exception as e:
            QMessageBox.critical(self, "Erro de Banco de Dados", f"Não foi possível carregar os veículos: {e}")
        finally:
            if conn: conn.close() 