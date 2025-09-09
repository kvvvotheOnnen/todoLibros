import random
from pathlib import Path
import sys
proyecto_root = Path(__file__).resolve().parent.parent  # Sube dos niveles: desde Antartica/ hasta raiz/
sys.path.append(str(proyecto_root))
from logs_templates.logs import process_logs, error_logs
import time
import pytz
from datetime import datetime
from rabbitmq_handler import RabbitMQHandler
from logic.randomScrap import scrapear_aleatoriamente

categorias = [
('https://miralibros.cl/a-narrativa','Narrativa'),
('https://miralibros.cl/b-poesia','Poesia'),
('https://miralibros.cl/c-salud-y-bienestar','salud_y_bienestar'),
('https://miralibros.cl/d-esoterismo-y-astrologia','Esoterismo_y_Astrologia'),
('https://miralibros.cl/e-negocios-y-finanzas','Negocios_y_Finanzas'),
('https://miralibros.cl/f-cocina','Cocina'),
('https://miralibros.cl/g-divulgacion-cientifica','Divulgacion_Cientifica'),
('https://miralibros.cl/h-naturaleza-y-ecologia','Naturaleza_y_Ecologia'),
('https://miralibros.cl/i-historia','Historia'),
('https://miralibros.cl/j-ciencias-humanas-y-sociales','Ciencias_Humanas_y_Sociales'),
('https://miralibros.cl/k-idiomas','Idiomas'),
('https://miralibros.cl/l-arte-y-arquitectura','Arte_y_Arquitectura'),
('https://miralibros.cl/m-tecnicas-artisticas-y-manualidades','Tecnicas_Artisticas_y_Manualidades'),
('https://miralibros.cl/n-musica','Musica'),
('https://miralibros.cl/o-cine','Cine'),
('https://miralibros.cl/p-comic-e-ilustracion','Comic_e_Ilustracion'),
('https://miralibros.cl/q-libros-infantiles','Libros_Infantiles'),
('https://miralibros.cl/r-papeleria-y-regalos','Papeleria_y_Regalos'),
('https://miralibros.cl/s-deportes','Deportes'),
('https://miralibros.cl/t-juegos','Juegos')
]

def main():
    while True:
        csv_filename = "MiraLibros.csv"
        csv_relative_path = f"data/{csv_filename}"
        start_time = datetime.now()
        process_logs(f"\n🚀 Iniciando ciclo de scraping - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        end_time = datetime.now()
        try:
            scrapear_aleatoriamente(categorias, 2)
        except ValueError as err:
            error_logs('en MiraLibros/scrapEmAll.py, flujo principal: ',err)
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