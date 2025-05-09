from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class MainAdmin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Painel do Administrador")
        self.setGeometry(200, 200, 400, 300)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        label = QLabel("Bem-vindo, Administrador!")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")

        layout.addWidget(label)
        self.setLayout(layout)
