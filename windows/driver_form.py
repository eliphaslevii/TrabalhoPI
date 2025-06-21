from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QDialogButtonBox
)

class DriverForm(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Adicionar Entregador")
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Formulário
        form_layout = QFormLayout()
        self.nome_input = QLineEdit()
        self.senha_input = QLineEdit()
        self.senha_input.setEchoMode(QLineEdit.Password) # Para esconder a senha

        form_layout.addRow("Nome:", self.nome_input)
        form_layout.addRow("Senha:", self.senha_input)
        layout.addLayout(form_layout)
        
        # Botões
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
            
    def get_data(self):
        """Retorna os dados do formulário."""
        return {
            'nome': self.nome_input.text().strip(),
            'senha': self.senha_input.text()
        } 