# auth_service.py
import time
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

class AuthService:
    @staticmethod
    def validate_credentials(user: str, password: str) -> bool:
        try:
            logging.info(f"Tentativa de login: usuário='{user}'")
            time.sleep(1)

            valid_users = {
                "admin": "123",
                "gestor": "456",
                "entregador": "789"
            }

            if user in valid_users and valid_users[user] == password:
                logging.info("Login autorizado.")
                return True
            else:
                logging.warning("Login negado: credenciais inválidas.")
                return False
        except Exception as e:
            logging.error(f"Erro ao validar usuário: {e}")
            return False

# opcional: expõe no nível de módulo
validate_credentials = AuthService.validate_credentials
