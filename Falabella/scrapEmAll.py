from pathlib import Path
import sys
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.append(str(project_root))
import config
import random
from logic.logs import error_logs, process_logs
import time
from datetime import datetime
from rabbitmq_handler import RabbitMQHandler
from logic.randomScrap import scrapear_aleatoriamente

categorias = [
    ('https://www.falabella.com/falabella-cl/category/CATG11448/Libros?page=1','general_falabella')
]


def main():
    while True:
        csv_filename = "Falabella.csv"
        csv_relative_path = f"data/{csv_filename}"
        start_time = datetime.now()
        process_logs(f"\n🚀 Iniciando ciclo de scraping - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        end_time = datetime.now()
        try:
            scrapear_aleatoriamente(categorias, 5, 2)
        except ValueError as err:
            error_logs('en Falabella/scrapEmAll.py, flujo principal: ',err)
        elapsed_time = end_time - start_time
        process_logs(f"⏳Tiempo total del scrap: {elapsed_time}")
        wait_hours = random.uniform(1, 4)
        wait_seconds = wait_hours * 3600
        process_logs(f"Esperando {wait_hours:.2f} horas para el próximo ciclo...⏳")
        time.sleep(wait_seconds)
        
        


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        process_logs("\n🔴 Script detenido manualmente")
        sys.exit(0)
    except Exception as e:
        process_logs(f"\n❌ Error no controlado: {str(e)}")
        sys.exit(1)