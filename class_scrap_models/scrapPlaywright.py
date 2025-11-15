import os
import time
import random
from playwright.sync_api import sync_playwright
from logic.export_to_csv import export_to_csv
from class_strategies.scrapStrategy import ScrapStrategy  
from logic.logs import error_logs, process_logs


class ScrapPlaywright:
    def __init__(self, url, strategy: ScrapStrategy, categoria="Generic"): 
        self.url = url
        self.categoria = categoria
        self.strategy = strategy  
        self.output_dir = os.getenv('OUTPUT_DIR', './data')
        os.makedirs(self.output_dir, exist_ok=True)
    

    def scrap(self):
        with sync_playwright() as p:
            try:
                browser = p.firefox.launch(headless=True)
                page = browser.new_page()
                page.goto(self.url)
                process_logs(f'Estamos en: {self.url}')
                selectors = self.strategy.get_selectors()
                page.wait_for_selector(selectors['product_container'], state="visible", timeout=60000)  
                while True:
                    tiempo_espera = int(random.uniform(5, 10))
                    try:
                        product_list =(self.strategy.get_products(page,self.categoria))
                        if product_list:
                            if self.strategy.needs_isbn_update():
                                process_logs('🔄 Actualizando ISBNs...')
                                product_list = self.strategy.update_products_isbn(browser, product_list)  # Pasa browser
                            process_logs(f'se obtuvieron: {len(product_list)} productos, ⏳esperando {tiempo_espera}s para la siguiente pagina' )
                            export_to_csv(product_list,self.categoria)
                            time.sleep(tiempo_espera)
                        if not self.strategy.next_page(page):
                            break   
                    except Exception as e:
                        error_logs(f'Error en el bucle principal de scrap', str(e))
                        break                      
            except Exception as e:
                error_logs('Error inicializando el navegador', str(e))
                
            finally:
                browser.close()

