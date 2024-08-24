from typing import List
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor

from app.models.cut_message import CutMessage

# Configurações do banco de dados
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'concorde'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'

def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return connection
    except Error as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None

def close_connection(connection):
    if connection:
        connection.close()

def fetch_data_from_db(query: str)-> List[CutMessage]:
    connection = create_connection()
    if connection:
        try:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query)
                records = cursor.fetchall()
                return records
        except Error as e:
            print(f"Erro ao executar a consulta SQL: {e}")
        finally:
            close_connection(connection)
    return None