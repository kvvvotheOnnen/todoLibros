import random
import sys
from pathlib import Path
# Obtiene la ruta absoluta de la raíz del proyecto (donde está "logs_templates")
proyecto_root = Path(__file__).resolve().parent.parent  # Sube dos niveles: desde Antartica/ hasta raiz/
sys.path.append(str(proyecto_root))
# Ahora puedes importar correctamente
from logic.logs import error_logs, process_logs
import time
import pytz
import sys
from datetime import datetime
import os
from rabbitmq_handler import RabbitMQHandler
from logic.randomScrap import scrapear_aleatoriamente
from class_scrap_models.scrapPlaywright import ScrapPlaywright
from class_strategies.antartica import Antartica
from logic.export_to_csv import export_to_csv 

categorias = [
('https://feriachilenadellibro.cl/categoria-producto/arte-y-diseno/','arte_y_diseno'),
('https://feriachilenadellibro.cl/categoria-producto/autoayuda/','autoayuda'),
('https://feriachilenadellibro.cl/categoria-producto/books-about-chile/','books_about_chile'),
('https://feriachilenadellibro.cl/categoria-producto/ciencia-y-naturaleza/', 'ciencia_y_naturaleza'),
('https://feriachilenadellibro.cl/categoria-producto/ciencias-sociales/','ciencias_sociales'),
('https://feriachilenadellibro.cl/categoria-producto/deportes/','deportes'),
('https://feriachilenadellibro.cl/categoria-producto/derecho/','derecho'),
('https://feriachilenadellibro.cl/categoria-producto/economia-y-negocios/','economia_y_negocios'),
('https://feriachilenadellibro.cl/categoria-producto/ensayos-y-biografias/','ensayos_y_biografias'),
('https://feriachilenadellibro.cl/categoria-producto/esoterismo/','esoterismo'),
('https://feriachilenadellibro.cl/categoria-producto/filosofia/','filosofia'),
('https://feriachilenadellibro.cl/categoria-producto/geografia/','geografia'),
('https://feriachilenadellibro.cl/categoria-producto/historia/','historia'),
('https://feriachilenadellibro.cl/categoria-producto/hogar-y-familia/','hogar_y_familia'),
('https://feriachilenadellibro.cl/categoria-producto/informatica-e-internet/','informatica_e_internet'),
('https://feriachilenadellibro.cl/categoria-producto/libros-infantiles/','libros_infantiles'),
('https://feriachilenadellibro.cl/categoria-producto/libros-juveniles/','libros_juveniles'),
('https://feriachilenadellibro.cl/categoria-producto/literatura/','literatura'),
('https://feriachilenadellibro.cl/categoria-producto/literatura-escolar/','literatura_escolar'),
('https://feriachilenadellibro.cl/categoria-producto/medicina/','medicina'),
('https://feriachilenadellibro.cl/categoria-producto/medicina-alternativa/','medicina_alternativa'),
('https://feriachilenadellibro.cl/categoria-producto/ocio-y-hobbies/','ocio_y_hobbies'),
('https://feriachilenadellibro.cl/categoria-producto/pack-de-libros/','pack_de_libros'),
('https://feriachilenadellibro.cl/categoria-producto/puzzles/','puzzles'),
('https://feriachilenadellibro.cl/categoria-producto/politica/','politica'),
('https://feriachilenadellibro.cl/categoria-producto/religion/','religion'),
('https://feriachilenadellibro.cl/categoria-producto/sexologia/','sexologia'),
('https://feriachilenadellibro.cl/categoria-producto/tecnologia/','tecnologia'),
('https://feriachilenadellibro.cl/categoria-producto/turismo-y-viajes/','turismo_y_viajes'),
]

def main():
    while True:
        csv_filename = "feriaChilena.csv"
        csv_relative_path = f"data/{csv_filename}"
        start_time = datetime.now()
        process_logs(f"\n🚀 Iniciando ciclo de scraping - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        end_time = datetime.now()
        try:
            scrapear_aleatoriamente(categorias, 3)
        except ValueError as err:
            error_logs('en feriaChilena/scrapEmAll.py, flujo principal: ',err)
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