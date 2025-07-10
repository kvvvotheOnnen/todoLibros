from scrap import Scrap
import random
from logs.logs import process_logs, error_logs
import time
import sys
from datetime import datetime
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

    try:
        scrap_unificador = Scrap('https://miralibros.cl', 'unificador')
        scrap_unificador.csv_forAll('miraLibros.csv')
    except Exception as e:
        error_logs('scrap unificador', f"Error al unir los CSV: {str(e)}")

def main():
    while True:
        start_time = datetime.now()
        process_logs(f"\n🚀 Iniciando ciclo de scraping - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        scrapear_aleatoriamente()
        
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
