import config
import random
from logic.logs import error_logs, process_logs
from class_strategies.antartica import Antartica
from class_strategies.miralibros import MiraLibros
from class_strategies.feriachilena import feriaChilena
from class_strategies.buscalibre import Buscalibre
from class_strategies.falabella import Falabella



import time
def scrapear_aleatoriamente(categorias, strategy, engine_type, max_reintentos=3):
    if engine_type == "playwright" or engine_type == 1:
        process_logs('Estrategia Playwright seleccionada')
        from class_scrap_models.scrapPlaywright import ScrapPlaywright
        ScrapClass = ScrapPlaywright
    elif engine_type == "selenium" or engine_type == 2:
        from class_scrap_models.scrapSeleniumBase import ScrapSeleniumBase
        ScrapClass = ScrapSeleniumBase
    else:
        raise ValueError(f"Tipo de engine no soportado: {engine_type}")
    
    
    categorias_procesadas = set()
    categorias_pendientes = categorias.copy()
    reintentos = {categoria: 0 for _, categoria in categorias}
    
    while categorias_pendientes:
        random.shuffle(categorias_pendientes)
        url, categoria = categorias_pendientes.pop()
        total_categorias = len(categorias)
        procesadas_actual = len(categorias_procesadas)
        process_logs(f"\n📌 Procesando ({procesadas_actual + 1}/{total_categorias}): {categoria}")
        
        try: #igual se podria hacer mejor la vd
            if strategy == 1:
                process_logs('Iniciando proceso con estrategia Playwright')
                playWrightScrap = ScrapClass(url, Antartica(), categoria)
                playWrightScrap.scrap()
                categorias_procesadas.add(categoria)
                process_logs(f"✅ Completado: {categoria}")
            if strategy == 2:
                process_logs('Iniciando proceso con estrategia Playwright')
                playWrightScrap = ScrapClass(url, MiraLibros(), categoria)
                playWrightScrap.scrap()
                categorias_procesadas.add(categoria)
                process_logs(f"✅ Completado: {categoria}")
            if strategy == 3:
                process_logs('Iniciando proceso con estrategia Playwright')
                playWrightScrap = ScrapClass(url, feriaChilena(), categoria)
                playWrightScrap.scrap()
                categorias_procesadas.add(categoria)
                process_logs(f"✅ Completado: {categoria}")
            if strategy == 4:
                process_logs('Iniciando proceso con estrategia SeleniumBase')
                playSeleniumBase = ScrapClass(url, Buscalibre(), categoria)
                playSeleniumBase.scrap()
                categorias_procesadas.add(categoria)
                process_logs(f"✅ Completado: {categoria}")
            if strategy == 5:
                process_logs('Iniciando proceso con estrategia SeleniumBase')
                playSeleniumBase = ScrapClass(url, Falabella(), categoria)
                playSeleniumBase.scrap()
                categorias_procesadas.add(categoria)
                process_logs(f"✅ Completado: {categoria}")
                
                
        except Exception as e:
            reintentos[categoria] += 1
            if reintentos[categoria] < max_reintentos:
                error_logs(f'scrapEmAll.py, while categorias pendientes', f"Reintentando ({reintentos[categoria]}/{max_reintentos}): {categoria}")
                categorias_pendientes.append((url, categoria))
            else:
                error_logs(f'scrapEmAll.py, while categorias pendientes', f"Fallo definitivo: {categoria}")
        
        if categorias_pendientes:
            delay = random.randint(8, 25)
            process_logs(f"⏳ Espera aleatoria: {delay}s")
            time.sleep(delay)

    process_logs("\n✅ Resultado final:")
    process_logs(f"- Categorías completadas: {len(categorias_procesadas)}/{len(categorias)}")
    
    # Mostrar categorías con reintentos
    categorias_con_reintentos = {cat: count for cat, count in reintentos.items() if count > 0}
    if categorias_con_reintentos:
        process_logs("- Reintentos necesarios:")
        for cat, count in categorias_con_reintentos.items():
            process_logs(f"  {cat}: {count} veces")
    
    return categorias_procesadas

