import logging
from database import create_connection

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

class AuthService:
    @staticmethod
    def validate_credentials(user: str, password: str) -> bool:
        try:
            logging.info(f"Tentativa de login: usuário='{user}'")


            conexao = create_connection()

            if conexao is None:
                logging.error("Não foi possível conectar ao banco de dados.")
                return False

            cursor = conexao.cursor()


            query = "SELECT * FROM users WHERE nome=%s AND senha=%s"
            cursor.execute(query, (user, password))
            result = cursor.fetchone()


            cursor.close()
            conexao.close()

            if result:
                logging.info("Login autorizado.")
                return True
            else:
                logging.warning("Login negado: credenciais inválidas.")
                return False

        except Exception as e:
            logging.error(f"Erro ao validar usuário: {str(e)}")
            return False
