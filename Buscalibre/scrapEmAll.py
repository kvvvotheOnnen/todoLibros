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
from logic.rabbitmq_handler import RabbitMQHandler
from logic.randomScrap import scrapear_aleatoriamente
from logic.csv_for_all import csv_forAll
import pytz


categorias = [
    ('https://www.buscalibre.cl/libros-mas-vendidos-en-chile_t.html', 'Libros mas vendidos en Chile'),
    ('https://www.buscalibre.cl/libros/infantiles-juveniles-didactico','Infantiles y Juveniles Didactico'),
]


def main():
    while True:
        csv_filename = "buscaLibre.csv"
        start_time = datetime.now()
        process_logs(f"\n🚀 Iniciando ciclo de scraping - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        try:
            scrapear_aleatoriamente(categorias, 4 ,2)
        except ValueError as err:
            error_logs('en buscaLibre/scrapEmAll.py, flujo principal: ',err)
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        process_logs(f"⏳Tiempo total del scrap: {elapsed_time}")
        wait_hours = random.uniform(1, 4)
        wait_seconds = wait_hours * 3600
        try:
            csv_success = csv_forAll("data", csv_filename)
            # if csv_success:
            #     try:
            #         with RabbitMQHandler() as rabbit:
            #             chile_tz = pytz.timezone("America/Santiago")
            #             timestamp = datetime.now(chile_tz).strftime("%d-%m-%Y %H:%M:%S")
            #             enviarACola = rabbit.send_csv_notification('Buscalibre', timestamp)
            #             if enviarACola:
            #                 process_logs('✅ CSV Buscalibre enviado a la cola exitosamente')
            #             else:
            #                 process_logs('❌ CSV Buscalibre no se envio a la cola de manera exitosa')
            #     except Exception as err:
            #         error_logs('proceso de cola rabbiMQ Buscalibre', err)
            # else:
            #     process_logs('❌ csv_forAll falló, no se envía a cola')

        except ValueError as ex:
            error_logs('Error en csv_forAll de Buscalibre', ex)
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