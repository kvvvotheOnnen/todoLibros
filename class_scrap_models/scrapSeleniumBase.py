import os
import time
import random
from seleniumbase import SB
from logic.export_to_csv import export_to_csv
from class_strategies.scrapStrategy import ScrapStrategy  
from logic.logs import error_logs, process_logs


class ScrapSeleniumBase:
    def __init__(self, url, strategy: ScrapStrategy, categoria="Generic"): 
        self.url = url
        self.categoria = categoria
        self.strategy = strategy  
        self.output_dir = os.getenv('OUTPUT_DIR', './data')
        os.makedirs(self.output_dir, exist_ok=True)
    
    
    def scrap(self):
        with SB(uc=True, headless=True) as sb: #AGREGAR EL XBVF EN PROD
            try:
                sb.open(self.url)
                process_logs(f'Estamos en: {self.url}')
                selectors = self.strategy.get_selectors()
                if sb .wait_for_element(selectors['product_container']):
                    process_logs('product_container cargado') 
                else: 
                    process_logs('no se carga product container')
                while True:
                    tiempo_espera = int(random.uniform(5, 10))
                    try:
                        current_results_url = sb.get_current_url()
                        product_list = self.strategy.get_products(sb,self.categoria)
                        if product_list:
                            if self.strategy.needs_isbn_update():
                                process_logs('🔄 Actualizando ISBNs...')
                                product_list = self.strategy.update_products_isbn(sb, product_list)  # Pasa browser
                                process_logs('🔄 Volviendo a la página de resultados...')
                                sb.open(current_results_url)
                                sb.wait_for_element(selectors['product_container'])
                            process_logs(f'se obtuvieron: {len(product_list)} productos, ⏳esperando {tiempo_espera}s para la siguiente pagina' )
                            export_to_csv(product_list,self.categoria)
                            time.sleep(tiempo_espera)
                        else: process_logs('No se encuentran productos')    
                        if not self.strategy.next_page(sb):
                            break   
                    except Exception as e:
                        error_logs(f'Error en el bucle principal de scrap', str(e))
                        break                      
            except Exception as e:
                error_logs('Error inicializando el navegador', str(e))
                
            finally:
                sb.disconnect()
