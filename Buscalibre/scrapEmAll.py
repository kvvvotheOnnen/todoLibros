from scrap import Scrap
from logs.logs import process_logs, error_logs
from datetime import datetime
import time
import random

categorias = [
    ('https://www.buscalibre.cl/libros-mas-vendidos-en-chile_t.html', 'Libros mas vendidos en Chile'),
    ('https://www.buscalibre.cl/libros/infantiles-juveniles-didactico','Infantiles y Juveniles Didactico'),
]

def main():
    start_time = datetime.now()
    process_logs(f"\n🚀 Iniciando ciclo de scraping - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    for idx, (url, categoria) in enumerate(categorias):
        process_logs(f"\n📌 Procesando: {categoria}")
        cat_start = datetime.now()
        scraper = Scrap(url, categoria)
        resultado = scraper.scrap()
        cat_end = datetime.now()
        elapsed = cat_end - cat_start
        elapsed_str = str(elapsed).split('.')[0]
        if resultado:
            process_logs(f"✅ Éxito: {categoria}")
        else:
            process_logs(f"❌ Fallo: {categoria}")
        process_logs(f"⏱ Tiempo para {categoria}: {elapsed_str}")
        if idx < len(categorias) - 1:
            espera = random.randint(30, 60)
            process_logs(f"⏳ Esperando {espera} segundos antes de la siguiente categoría...")
            time.sleep(espera)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    process_logs(f"⏱ Tiempo total del ciclo: {elapsed_time}")

    # Unir todos los CSV generados en un solo archivo
    try:
        scrap_unificador = Scrap('https://www.buscalibre.cl', 'unificador')
        scrap_unificador.csv_forAll('Buscalibre.csv')
    except Exception as e:
        error_logs('scrap unificador', f"Error al unir los CSV: {str(e)}")

if __name__ == "__main__":
    main()