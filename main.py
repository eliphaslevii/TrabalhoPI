import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox, QFormLayout, QCheckBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSettings


# TELA DE LOGIN
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 150)
        self.settings = QSettings("PI","App")
        self.init_ui()
        self.triggerFocus()
        self.loadCredentials()

    def init_ui(self):
        layout = QFormLayout()


        #label/Input Username
        self.label_user = QLabel("Usuário:")
        self.input_user = QLineEdit()
        #self.input_user.setMinimumHeight(50)
        #self.input_user.setFont(QFont("Verdana",10,QFont.Bold))

        #label/input Password
        self.label_pass = QLabel("Senha:")
        self.input_pass = QLineEdit()

        self.input_pass.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Entrar")
        self.login_button.clicked.connect(self.login)

        #checkBox Remember-me
        self.rememberMe = QCheckBox()
        self.rememberMeLabel = QLabel("Lembrar-me")


        layout.addRow(self.label_user)
        layout.addRow(self.input_user)
        layout.addRow(self.label_pass)
        layout.addRow(self.input_pass)
        layout.addRow(self.rememberMe,self.rememberMeLabel)
        layout.addRow(self.login_button)

        self.setLayout(layout)

    def login(self):
        username = self.input_user.text()
        password = self.input_user.text()
        if username == 'admin' and password == 'admin':
            if self.rememberMe.isChecked():
                self.triggerRememberMe(username,password)
            else:
                self.input_pass.setText("")
                self.input_user.setText("")
                self.rememberMe.setChecked(False)
                return
    def triggerRememberMe(self,username,password):
            if self.rememberMe.isChecked():
                self.settings.setValue('username',username)
                self.settings.setValue('password',password)
                self.settings.setValue('remember',True)

    def loadCredentials(self):
        remember = self.settings.value("remember", False, type=bool)
        if remember:
            self.input_user.setText(self.settings.value("username", ""))
            self.input_pass.setText(self.settings.value("password", ""))
            self.rememberMe.setChecked(True)

    def triggerFocus(self):
        self.input_user.setFocus()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
