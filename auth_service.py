import logging
import time
from database import create_connection

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

class AuthService:
    @staticmethod
    def validate_credentials(user: str, password: str) -> bool:
        """
        Retorna True se 'user' e 'password' forem encontrados na tabela users.
        Simula 3s de latência e faz log das tentativas.
        """
        logging.info(f"Tentativa de login: usuário='{user}'")
        time.sleep(3)  # apenas para simular processamento

        conn = create_connection()
        if not conn:
            return False

        cursor = conn.cursor()
        cursor.execute(
            "SELECT nivel FROM users WHERE nome = %s AND senha = %s",
            (user, password)
        )
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            logging.info("Login autorizado.")
            return True
        else:
            logging.warning("Login negado: credenciais inválidas.")
            return False
