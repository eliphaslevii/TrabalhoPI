# auth_service.py
import time
import logging
from database import create_connection

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

class AuthService:
    @staticmethod
    def validate_credentials(user: str, password: str) -> bool:
        """
        Valida as credenciais do usuário no banco de dados.
        Retorna True se as credenciais forem válidas, False caso contrário.
        """
        conn = create_connection()
        if not conn:
            return False

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE nome=%s AND senha=%s", (user, password))
                result = cursor.fetchone()
                return result is not None
        except Exception as e:
            logging.error(f"Erro ao validar credenciais: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def get_user_level(user: str) -> int:
        """
        Retorna o nível de permissão do usuário (1 para admin, 2 para entregador).
        Retorna None se o usuário não for encontrado.
        """
        conn = create_connection()
        if not conn:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT nivel FROM users WHERE nome=%s", (user,))
                result = cursor.fetchone()
                return result['nivel'] if result else None
        except Exception as e:
            logging.error(f"Erro ao buscar nível do usuário: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def is_admin(user: str) -> bool:
        """
        Verifica se o usuário é um administrador.
        """
        level = AuthService.get_user_level(user)
        return level == 1

# opcional: expõe no nível de módulo
validate_credentials = AuthService.validate_credentials
