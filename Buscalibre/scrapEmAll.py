from scrap import Scrap
from logs.logs import process_logs
from datetime import datetime

categorias = [
    ('https://www.buscalibre.cl/libros-mas-vendidos-en-chile_t.html', 'Libros mas vendidos en Chile'),
    ('https://www.buscalibre.cl/libros/infantiles-juveniles-didactico','Infantiles y Juveniles Didactico'),
]

def main():
    start_time = datetime.now()
    process_logs(f"\n🚀 Iniciando ciclo de scraping - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    for url, categoria in categorias:
        process_logs(f"\n📌 Procesando: {categoria}")
        scraper = Scrap(url, categoria)
        resultado = scraper.scrap()
        if resultado:
            process_logs(f"✅ Éxito: {categoria}")
        else:
            process_logs(f"❌ Fallo: {categoria}")
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    process_logs(f"⏱ Tiempo total del ciclo: {elapsed_time}")

if __name__ == "__main__":
    main()