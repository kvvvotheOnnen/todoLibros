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
        try:
            scrapear_aleatoriamente(categorias, 3,1)
        except ValueError as err:
            error_logs('en feriaChilena/scrapEmAll.py, flujo principal: ',err)
        end_time = datetime.now()
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