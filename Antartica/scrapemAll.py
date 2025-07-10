from scrap import Scrap
import random
from logs.logs import process_logs, error_logs
import time
import sys
from datetime import datetime

categorias = [
    ('https://www.antartica.cl/libros/arte-y-arquitectura.html', 'Arte y Arquitectura'),
    ('https://www.antartica.cl/libros/economia-y-administracion.html','Economia y administracion'),
    ('https://www.antartica.cl/libros/entretencion-y-manual.html','Entretencion y manualidades'),
    ('https://www.antartica.cl/libros/gastronomia-y-vinos.html','Gastronomia y vinos'),
    ('https://www.antartica.cl/libros/literatura.html','Literatura'),
    ('https://www.antartica.cl/libros/mundo-comic.html','Mundo comic'),
    ('https://www.antartica.cl/libros/ciencias/ciencias-agrarias-y-de-la-naturaleza.html', 'Ciencias agrarias y de la naturaleza'),
    ('https://www.antartica.cl/libros/ciencias-exactas/ciencias-fisicas-y-elementales.html', 'Ciencias físicas y elementales'),
    ('https://www.antartica.cl/libros/ciencias-exactas/ingenieria-y-tecnologia.html', 'Ingeniería y tecnología'),
    ('https://www.antartica.cl/libros/ciencias/ciencias-medicas.html', 'Ciencias médicas'),
    ('https://www.antartica.cl/libros/ciencias/zoologia-y-animales-domesticos.html', 'Zoología y animales domésticos'),
    ('https://www.antartica.cl/libros/computacion-e-informacion/conectados.html', 'Conectados'),
    ('https://www.antartica.cl/libros/computacion-e-informacion/informatica.html', 'Informática'),
    ('https://www.antartica.cl/libros/cuerpo-y-mente/autoayuda.html', 'Autoayuda'),
    ('https://www.antartica.cl/libros/cuerpo-y-mente/ciencias-alternativas-y-esoterismo.html', 'Ciencias alternativas y esoterismo'),
    ('https://www.antartica.cl/libros/guias-de-viaje-y-tur/guias-de-viaje.html', 'Guías de viaje'),
    ('https://www.antartica.cl/libros/guias-de-viaje-y-tur/mapas-y-planos.html', 'Mapas y planos'),
    ('https://www.antartica.cl/libros/infantil-y-juvenil/juegos-ocio-y-actividades.html', 'Juegos, ocio y actividades'),
    ('https://www.antartica.cl/libros/infantil-y-juvenil/libros-infantiles.html', 'Libros infantiles'),
    ('https://www.antartica.cl/libros/infantil-y-juvenil/literatura-juvenil.html', 'Literatura juvenil'),
    ('https://www.antartica.cl/libros/referencias/diccionarios.html', 'Diccionarios'),
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
                error_logs(f'scrapEmAll.py, while categorias pendientes',"Reintentando ({reintentos[categoria]}/{max_reintentos}): {categoria}")
                categorias_pendientes.append((url, categoria))
            else:
                error_logs(f'scrapEmAll.py, while categorias pendientes',"Fallo definitivo: {categoria}")
        
        if categorias_pendientes:
            delay = random.randint(8, 25)  # Rango más amplio
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
        
        try:
            scrap_unificador = Scrap('https://www.antartica.cl', 'unificador')
            scrap_unificador.csv_forAll('Antartica.csv')
        except Exception as e:
            error_logs(f'scrap unificador',"Error al unir los CSV: {str(e)}")
        
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        process_logs(f"⏱ Tiempo total del ciclo: {elapsed_time}")
        
        wait_hours = random.uniform(1, 4)
        wait_seconds = int(wait_hours * 3600)
        process_logs(f"⏳ Esperando {wait_hours:.2f} horas para el próximo ciclo...")
        
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