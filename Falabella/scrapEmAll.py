from scrap import Scrap
import random
from logs_templates.logs import process_logs, error_logs
import time
import pytz
import sys
from datetime import datetime
import os
from rabbitmq_handler import RabbitMQHandler

categorias = [
('https://www.falabella.com/falabella-cl/category/CATG11448/Libros?page=1','general_falabella')
]

def on_csv_generated(csv_path, service_name):
    try:
        with RabbitMQHandler() as rabbit:  # Conexión automática
            chile_tz = pytz.timezone("America/Santiago")
            timestamp = datetime.now(chile_tz).strftime("%d-%m-%Y %H:%M:%S")
            rabbit.send_csv_notification(
                service_name=service_name,
                csv_path=csv_path,
                timestamp=timestamp
            )
    except Exception as e:
        error_logs(f"Error en on_csv_generated: {str(e)}")  

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

    # Unir todos los CSV generados en un solo archivo
        try:
            scrap_unificador = Scrap('https://www.falabella.cl', 'unificador')
            if scrap_unificador.csv_forAll(csv_filename):
                if os.path.exists(csv_relative_path):
                            on_csv_generated(
                            csv_path=os.path.abspath(csv_relative_path),  # Convierte a ruta absoluta
                            service_name="Falabella"
                            )
                else:
                    process_logs(f"❌ Archivo CSV no encontrado en {csv_relative_path}")    
            else:
                process_logs("❌ Fallo al generar el CSV")
        except Exception as e:
            error_logs(f"Error al unir los CSV: ", {str(e)})

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
