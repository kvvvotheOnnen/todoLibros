import os
from playwright.sync_api import sync_playwright
from logic.export_to_csv import export_to_csv
from class_strategies.scrapStrategy import ScrapStrategy  # Importamos la clase abstracta
from logs_templates.logs import error_logs, process_logs


class ScrapPlaywright:
    def __init__(self, url, strategy: ScrapStrategy, categoria="Generic"): #la estregia esperada es del tipo ScrapStrategy
        self.url = url
        self.categoria = categoria
        self.strategy = strategy  # aqui va la estrategia especifica
        self.output_dir = os.getenv('OUTPUT_DIR', './data')
        os.makedirs(self.output_dir, exist_ok=True)
    
    
    def scrap(self):
        with sync_playwright() as p:
            try:
                browser = p.firefox.launch(headless=True)
                page = browser.new_page()
                page.goto(self.url)
                # Usamos los selectores de la estrategia
                process_logs(f'Estamos en: {self.url}')
                selectors = self.strategy.get_selectors()
                page.wait_for_selector(selectors['product_container'], state="visible", timeout=60000)  
                while True:
                    try:
                        # Delegamos la extracción a la estrategia
                        product_list =(self.strategy.get_products(page,self.categoria))
                        if product_list:
                            process_logs(f'se obtuvieron: {len(product_list)} productos' )
                            export_to_csv(product_list,self.categoria)
                        if not self.strategy.next_page(page):
                            break   
                    except Exception as e:
                        error_logs(f'Error en el bucle principal de scrap', str(e))
                        break                      
            except Exception as e:
                error_logs('Error inicializando el navegador', str(e))
                
            finally:
                browser.close()

