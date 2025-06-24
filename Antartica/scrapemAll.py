from scrap import Scrap
import random
from logs.logs import process_logs
import time
import sys
from datetime import datetime

categorias = [
    ('https://www.antartica.cl/libros/arte-y-arquitectura.html', 'Arte y Arquitectura'),
    ('https://www.antartica.cl/libros/ciencias.html', 'Ciencias'),
    ('https://www.antartica.cl/libros/ciencias-exactas.html','Ciencias Exactas'),
    ('https://www.antartica.cl/libros/computacion-e-informacion.html','Computacion e informatica'),
    ('https://www.antartica.cl/libros/cuerpo-y-mente.html','Cuerpo y mente'),
    ('https://www.antartica.cl/libros/economia-y-administracion.html','Economia y administracion'),
    ('https://www.antartica.cl/libros/entretencion-y-manual.html','Entretencion y manualidades'),
    ('https://www.antartica.cl/libros/gastronomia-y-vinos.html','Gastronomia y vinos'),
    ('https://www.antartica.cl/libros/guias-de-viaje-y-tur.html','Guias de viaje y turismo'),
    ('https://www.antartica.cl/libros/infantil-y-juvenil.html','Infantil y juvenil'),
    ('https://www.antartica.cl/libros/literatura.html','Literatura'),
    ('https://www.antartica.cl/libros/mundo-comic.html','Mundo comic'),
    ('https://www.antartica.cl/libros/referencias.html','Referencias')
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