import os
import sys
from datetime import datetime

def error_logs(location, error_message, force_file=False):

    timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    log_entry = f"[{timestamp}] Error en: {location}: {error_message}"
    # Siempre a stderr (consola/Docker)
    print(log_entry, file=sys.stderr)
    
    if os.getenv('ENVIRONMENT') == 'development' or force_file:
        log_path = os.getenv('LOG_FILE_PATH', './logs.txt')
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')
        except Exception as e:
            print(f"[ERROR] No se pudo escribir en {log_path}: {str(e)}", file=sys.stderr)

def process_logs(process_message, force_file=False):

    timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    log_entry = f"[{timestamp}] {process_message}"
    # Siempre a stderr (consola/Docker)
    print(log_entry, file=sys.stderr)
    
    if os.getenv('ENVIRONMENT') == 'development' or force_file:
        log_path = os.getenv('LOG_FILE_PATH', './logs.txt')
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')
        except Exception as e:
            print(f"[ERROR] No se pudo escribir en {log_path}: {str(e)}", file=sys.stderr)