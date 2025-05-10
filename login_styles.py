def get_dark_theme_styles():
    return """
        QWidget {
            background-color: #2b2b2b;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        QLabel {
            color: #ffffff;
            font-size: 11px;
            font-weight: normal;
        }
        QLineEdit {
            padding: 8px;
            padding-left: 10px;
            border: 1px solid #404040;
            border-radius: 5px;
            background-color: #3b3b3b;
            color: #ffffff;
            font-size: 11px;
            text-align: left;
        }
        QLineEdit::placeholder {
            color: rgba(255, 255, 255, 0.3);
            text-align: left;
        }
        QLineEdit:focus {
            border: 2px solid #2196F3;
        }
        QPushButton {
            background-color: #2196F3;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            font-size: 12px;
            font-weight: bold;
            min-width: 100px;
        }
        QPushButton:hover {
            background-color: #1976D2;
        }
        QPushButton:pressed {
            background-color: #1565C0;
        }
        QCheckBox {
            color: #ffffff;
            font-size: 10px;
            font-weight: normal;
        }
        QCheckBox::indicator {
            width: 14px;
            height: 14px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 3px;
            background-color: #3b3b3b;
        }
        QCheckBox::indicator:unchecked {
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 3px;
            background-color: #3b3b3b;
        }
        QCheckBox::indicator:checked {
            background-color: #2196F3;
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 3px;
        }
        QCheckBox::indicator:hover {
            border: 1px solid rgba(255, 255, 255, 0.5);
        }
        QProgressBar {
            border: none;
            background-color: #404040;
            border-radius: 1px;
        }
        QProgressBar::chunk {
            background-color: #2196F3;
            border-radius: 1px;
        }
        #theme_button {
            border: none;
            background-color: transparent;
            border-radius: 12px;
        }
        #theme_button:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
        #theme_button:pressed {
            background-color: rgba(255, 255, 255, 0.2);
        }
    """

def get_light_theme_styles():
    return """
        QWidget {
            background-color: #f0f0f0;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        QLabel {
            color: #000000;
            font-size: 11px;
            font-weight: normal;
        }
        QLineEdit {
            padding: 8px;
            padding-left: 10px;
            border: 1px solid #cccccc;
            border-radius: 5px;
            background-color: white;
            font-size: 11px;
            text-align: left;
        }
        QLineEdit::placeholder {
            color: rgba(0, 0, 0, 0.3);
            text-align: left;
        }
        QLineEdit:focus {
            border: 2px solid #808080;
        }
        QPushButton {
            background-color: #2196F3;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            font-size: 12px;
            font-weight: bold;
            min-width: 100px;
        }
        QPushButton:hover {
            background-color: #1976D2;
        }
        QPushButton:pressed {
            background-color: #1565C0;
        }
        QCheckBox {
            color: #000000;
            font-size: 10px;
            font-weight: normal;
        }
        QCheckBox::indicator {
            width: 14px;
            height: 14px;
            border: 1px solid rgba(128, 128, 128, 0.3);
            border-radius: 3px;
            background-color: white;
        }
        QCheckBox::indicator:unchecked {
            border: 1px solid rgba(128, 128, 128, 0.3);
            border-radius: 3px;
            background-color: white;
        }
        QCheckBox::indicator:checked {
            background-color: #2196F3;
            border: 1px solid rgba(128, 128, 128, 0.3);
            border-radius: 3px;
        }
        QCheckBox::indicator:hover {
            border: 1px solid rgba(128, 128, 128, 0.5);
        }
        QProgressBar {
            border: none;
            background-color: #E0E0E0;
            border-radius: 1px;
        }
        QProgressBar::chunk {
            background-color: #2196F3;
            border-radius: 1px;
        }
        #theme_button {
            border: none;
            background-color: transparent;
            border-radius: 12px;
        }
        #theme_button:hover {
            background-color: rgba(0, 0, 0, 0.1);
        }
        #theme_button:pressed {
            background-color: rgba(0, 0, 0, 0.2);
        }
    """ 