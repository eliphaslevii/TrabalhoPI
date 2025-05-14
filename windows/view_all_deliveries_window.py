from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton

class ViewAllDeliveriesWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Todas as Entregas")
        self.setGeometry(100, 100, 400, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        close_btn = QPushButton("Fechar")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn) 