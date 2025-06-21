def get_login_styles():
    """Retorna uma string QSS para a janela de login."""
    return """
        QWidget {
            background-color: #f0f0f0;
        }
        QLabel#title_label {
            font-size: 24pt;
            font-weight: bold;
            color: #1e1e1e;
            padding-bottom: 20px;
        }
        QLabel {
            font-size: 11pt;
            color: #333;
        }
        QLineEdit {
            background-color: #ffffff;
            border: 1px solid #dcdcdc;
            padding: 8px 8px 8px 35px; /* Padding à esquerda para o ícone */
            border-radius: 4px;
            font-size: 11pt;
        }
        QPushButton {
            background-color: #0078d7;
            color: #ffffff;
            border: none;
            padding: 10px;
            border-radius: 4px;
            font-size: 11pt;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #005a9e;
        }
        QPushButton:pressed {
            background-color: #004578;
        }
    """ 