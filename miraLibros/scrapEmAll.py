from scrap import Scrap
import random
from logs.logs import process_logs, error_logs
import time
import sys
from datetime import datetime
import os
from rabbitmq_handler import RabbitMQHandler
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
# Después de generar el CSV exitosamente
def on_csv_generated(csv_path, service_name):
    rabbit = RabbitMQHandler()
    if rabbit.connect():
        timestamp = datetime.now().isoformat()
        rabbit.send_csv_notification(
            service_name=service_name,
            csv_path=csv_path,
            timestamp=timestamp
        )
        rabbit.close()

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
        csv_filename = "miraLibros.csv" #Dato dinamico, ajustar a lo que agrege despues
        csv_relative_path = f"data/{csv_filename}"
        start_time = datetime.now()
        process_logs(f"\n🚀 Iniciando ciclo de scraping - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        scrapear_aleatoriamente()
        
        try:
            scrap_unificador = Scrap('https://www.miralibros.cl', 'unificador') #Dato dinamico, ajustar a lo que agrege despues
            if scrap_unificador.csv_forAll(csv_filename):
                if os.path.exists(csv_relative_path): 
                            on_csv_generated(
                            csv_path=os.path.abspath(csv_relative_path),  # Convierte a ruta absoluta
                            service_name="miraLibros"
                            )
                else:
                    process_logs(f"❌ Archivo CSV no encontrado en {csv_relative_path}")    
            else:
                process_logs("❌ Fallo al generar el CSV")
        except Exception as e:
            error_logs(f'scrap unificador',"Error al unir los CSV: {str(e)}")
        
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