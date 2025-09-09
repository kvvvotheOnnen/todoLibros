import os
from datetime import datetime

LOG_DIR = os.getenv("LOG_DIR", os.getcwd()) 
LOG_FILENAME = os.getenv("LOG_FILENAME", "logs.txt")  
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILENAME) 

def _write_log_entry(message: str):
    """Función interna para escribir en el log."""
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        

        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    except Exception as e:
        print(f"Error escribiendo log: {str(e)}") 

def error_logs(location: str, error_message: str):
    """Registra errores. Siempre guarda en archivo, sin prints."""
    timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    log_entry = f"[{timestamp}] Error en: {location}: {error_message}"
    _write_log_entry(log_entry)  

def process_logs(process_message: str):
    """Registra procesos. Siempre guarda en archivo, sin prints."""
    timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    log_entry = f"[{timestamp}] Proceso: {process_message}"
    _write_log_entry(log_entry)  