from scrap import Scrap
import random
from logs.logs import process_logs
import time
import sys
from datetime import datetime
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
('https://feriachilenadellibro.cl/categoria-producto/material-didactico/','material_didactico'),
('https://feriachilenadellibro.cl/categoria-producto/pack-de-libros/','pack_de_libros'),
('https://feriachilenadellibro.cl/categoria-producto/puzzles/','puzzles'),
('https://feriachilenadellibro.cl/categoria-producto/politica/','politica'),
('https://feriachilenadellibro.cl/categoria-producto/religion/','religion'),
('https://feriachilenadellibro.cl/categoria-producto/sexologia/','sexologia'),
('https://feriachilenadellibro.cl/categoria-producto/tecnologia/','tecnologia'),
('https://feriachilenadellibro.cl/categoria-producto/texto-de-estudio/','texto_de_estudio'),
('https://feriachilenadellibro.cl/categoria-producto/turismo-y-viajes/','turismo_y_viajes'),
]

def scrapear_aleatoriamente(max_reintentos=3):
    categorias_procesadas = set()
    categorias_pendientes = categorias.copy()
    reintentos = {categoria: 0 for _, categoria in categorias}
    
    while categorias_pendientes:
        random.shuffle(categorias_pendientes)
        url, categoria = categorias_pendientes.pop()
        
        process_logs(f"\n📌 Procesando ({len(categorias_procesadas)+1}/{len(categorias)}): {categoria}")
        scraper = Scrap(url, categoria)
        
        try:
            scraper.scrap()
            categorias_procesadas.add(categoria)
            process_logs(f"Éxito: {categoria}")
        except Exception as e:
            reintentos[categoria] += 1
            if reintentos[categoria] < max_reintentos:
                process_logs(f"Reintentando ({reintentos[categoria]}/{max_reintentos}): {categoria}")
                categorias_pendientes.append((url, categoria))
            else:
                process_logs(f"Fallo definitivo: {categoria}")
        
        if categorias_pendientes:
            delay = random.randint(8, 25)  
            process_logs(f"Espera aleatoria: {delay}s")
            time.sleep(delay)

    process_logs("\n✅ Resultado final:")
    process_logs(f"- Categorías completadas: {len(categorias_procesadas)}/{len(categorias)}")
    if reintentos:
        process_logs("- Reintentos necesarios:")
        for cat, count in reintentos.items():
            if count > 0:
                process_logs(f"  {cat}: {count} veces")

def main():
    while True:
        start_time = datetime.now()
        process_logs(f"\n🚀 Iniciando ciclo de scraping - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        scrapear_aleatoriamente()
        
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        process_logs(f"⏱ Tiempo total del ciclo: {elapsed_time}")
        
        # Espera aleatoria entre 1 y 4 horas (3600 a 14400 segundos)
        wait_hours = random.uniform(1, 4)
        wait_seconds = int(wait_hours * 3600)
        process_logs(f"⏳ Esperando {wait_hours:.2f} horas para el próximo ciclo...")
        
        # Espera mostrando progreso cada 5 minutos
        for remaining in range(wait_seconds, 0, -300):
            minutes_left = remaining // 60
            process_logs(f"🕒 Próximo ciclo en ~{minutes_left} minutos...")
            time.sleep(min(300, remaining))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        process_logs("\n🔴 Script detenido manualmente")
        sys.exit(0)
    except Exception as e:
        process_logs(f"\n❌ Error no controlado: {str(e)}")
        sys.exit(1)
