import os
import psycopg2
from dotenv import load_dotenv
from logic.logs import error_logs, process_logs

# Carga las variables de entorno desde el archivo .env
load_dotenv()

def get_db_connection():
    """
    Establece y devuelve una conexión a la base de datos PostgreSQL.
    Lee los parámetros de conexión de las variables de entorno.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT", 5432) # Puerto por defecto de PostgreSQL
        )
        process_logs("✅ Conexión a la base de datos PostgreSQL exitosa.")
        return conn
    except psycopg2.OperationalError as e:
        error_logs(f"❌ Error al conectar con la base de datos: {e}")
        return None
    except Exception as e:
        error_logs(f"❌ Ocurrió un error inesperado en la conexión a la base de datos: {e}")
        return None