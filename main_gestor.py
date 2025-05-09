from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class MainGestor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Painel do Gestor")
        self.setGeometry(100, 100, 400, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Bem-vindo ao painel do Gestor!")
        layout.addWidget(label)
        self.setLayout(layout)
