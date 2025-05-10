from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class MainEntregador(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Painel do Entregador")
        self.setGeometry(100, 100, 400, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Bem-vindo ao painel do Entregador!")
        layout.addWidget(label)
        self.setLayout(layout)