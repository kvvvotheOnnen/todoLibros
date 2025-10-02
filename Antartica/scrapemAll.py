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
from logic.csv_for_all import csv_forAll


categorias = [
   #('https://www.antartica.cl/libros/arte-y-arquitectura.html', 'Arte y Arquitectura'),
   #('https://www.antartica.cl/libros/economia-y-administracion.html','Economia y administracion'),
   ('https://www.antartica.cl/libros/entretencion-y-manual.html','Entretencion y manualidades'),
   ('https://www.antartica.cl/libros/gastronomia-y-vinos.html','Gastronomia y vinos'),
   #('https://www.antartica.cl/libros/literatura.html','Literatura'),
   #('https://www.antartica.cl/libros/mundo-comic.html','Mundo comic'),
   #('https://www.antartica.cl/libros/ciencias/ciencias-agrarias-y-de-la-naturaleza.html', 'Ciencias agrarias y de la naturaleza'),
   #('https://www.antartica.cl/libros/ciencias-exactas/ciencias-fisicas-y-elementales.html', 'Ciencias físicas y elementales'),
   #('https://www.antartica.cl/libros/ciencias-exactas/ingenieria-y-tecnologia.html', 'Ingeniería y tecnología'),
   #('https://www.antartica.cl/libros/ciencias/ciencias-medicas.html', 'Ciencias médicas'),
   #('https://www.antartica.cl/libros/ciencias/zoologia-y-animales-domesticos.html', 'Zoología y animales domésticos'),
   #('https://www.antartica.cl/libros/computacion-e-informacion/conectados.html', 'Conectados'),
   #('https://www.antartica.cl/libros/computacion-e-informacion/informatica.html', 'Informática'),
   #('https://www.antartica.cl/libros/cuerpo-y-mente/autoayuda.html', 'Autoayuda'),
   #('https://www.antartica.cl/libros/cuerpo-y-mente/ciencias-alternativas-y-esoterismo.html', 'Ciencias alternativas y esoterismo'),
   ('https://www.antartica.cl/libros/guias-de-viaje-y-tur/guias-de-viaje.html', 'Guías de viaje'),
   #('https://www.antartica.cl/libros/guias-de-viaje-y-tur/mapas-y-planos.html', 'Mapas y planos'),
   #('https://www.antartica.cl/libros/infantil-y-juvenil/juegos-ocio-y-actividades.html', 'Juegos, ocio y actividades'),
   #('https://www.antartica.cl/libros/infantil-y-juvenil/libros-infantiles.html', 'Libros infantiles'),
   #('https://www.antartica.cl/libros/infantil-y-juvenil/literatura-juvenil.html', 'Literatura juvenil'),
   #('https://www.antartica.cl/libros/referencias/diccionarios.html', 'Diccionarios')
]

def main():
    while True:
        csv_filename = "Antartica.csv"
        start_time = datetime.now()
        process_logs(f"\n🚀 Iniciando ciclo de scraping - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        try:
            scrapear_aleatoriamente(categorias, 1, 1)
        except ValueError as err:
            error_logs('en Antartica/scrapEmAll.py, flujo principal: ',err)
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        process_logs(f"⏳Tiempo total del scrap: {elapsed_time}")
        wait_hours = random.uniform(1, 4)
        wait_seconds = wait_hours * 3600
        try:
            csv_forAll("data",csv_filename)
        except ValueError as ex:
            error_logs('Error en csv_forAll de Antartica', ex)
        finally:
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