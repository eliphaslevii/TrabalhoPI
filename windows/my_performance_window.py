from PyQt5.QtWidgets import QDialog

class MyPerformanceWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Meu Desempenho")
        self.setFixedSize(400, 400) 