import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    try:
        conect = mysql.connector.connect(
            host=os.getenv("HOST_DB", "localhost"),
            user=os.getenv("USER_DB"),
            password=os.getenv("PASSWORD_DB"),
            database=os.getenv("DATABASE_DB"),
            port=int(os.getenv("PORT_DB", 3306)),
            raise_on_warnings=True
        )
        return conect

    except mysql.connector.Error as erro:
        print(f'Erro ao conectar ao MySQL: {erro}')
