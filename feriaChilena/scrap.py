import re
import time
import random
from logs.logs import error_logs, process_logs
import os
import csv
from playwright.sync_api import sync_playwright
class Scrap():
    def __init__(self, url, categoria):
        self.url = url
        self.categoria = categoria
        self.output_dir = os.getenv('OUTPUT_DIR', './data') 
        os.makedirs(self.output_dir, exist_ok=True)

    def extraer_isbn(self,url):
        match = re.search(r"/(\d+)-", url)
        if match:
            return match.group(1)  
        return None  

    def pasar_pagina(self, page):
        next_btn = page.query_selector('a.next.page-numbers')
        if not next_btn:
            return False

        next_btn.click()
        page.wait_for_selector('li.product')  
        return True

    def export_to_csv(self, products):
        try:
            filename = os.path.join(self.output_dir, f"{self.categoria.replace(' ', '_')}.csv")

            with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['isbn', 'titulo', 'Autor', 'precio', 'link', 'categoria']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                
                writer.writeheader()
                
                for product in products:
                    product_data = product.copy()
                    writer.writerow(product_data)
            if os.path.exists(filename):
                process_logs(f"Archivo cvs creado exitosamente: {filename}")
                process_logs(f"📊 Total de registros guardados: {len(products)}")
                return filename
            else:
                error_logs('El archivo CSV no se creó correctamente', '')
                return None

        except Exception as err:  
            error_logs('Error en export_to_csv', str(err))
        return None

    def csv_forAll(self, nombre_csv_final):
        archivos = [f for f in os.listdir(self.output_dir) if f.endswith('.csv')]
        if not archivos:
            process_logs(f'No se encontraron archivos CSV en {self.output_dir}')
            return

        cabecera = None
        filas = []

        for archivo in archivos:
            ruta_archivo = os.path.join(self.output_dir, archivo)
            with open(ruta_archivo, newline='', encoding='utf-8') as f:
                lector = csv.reader(f)
                try:
                    cabecera_archivo = next(lector)
                except StopIteration:
                    continue  # archivo vacío
                if cabecera is None:
                    cabecera = cabecera_archivo
                elif cabecera != cabecera_archivo:
                    process_logs(f"Advertencia: la cabecera de {archivo} es diferente. Se ignorará este archivo.")
                    continue
                filas.extend(list(lector))

        if cabecera is None:
            process_logs('No se pudo determinar la cabecera de los archivos CSV.')
            return

        ruta_final = os.path.join(self.output_dir, nombre_csv_final)
        with open(ruta_final, 'w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            escritor.writerow(cabecera)
            escritor.writerows(filas)
        process_logs(f'Se creó el archivo {ruta_final} con {len(filas)} filas.')


    def scrap(self):
        products = []
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(self.url)
                page.wait_for_selector(".ast-woocommerce-container", state="visible", timeout=60000)
                while True:
                    try:
                        product_cards = page.query_selector_all(
                            'li.ast-col-sm-12.ast-article-post.product.type-product.has-post-thumbnail'
                        )                        
                        process_logs(f"📚 Procesando {len(product_cards)} productos en la página actual")
                        
                        for element in product_cards:
                            try:
                                link = element.query_selector("a.ast-loop-product__link").get_attribute("href")
                                price_element = element.query_selector("span.price .woocommerce-Price-amount")
                                price = price_element.inner_text().strip() if price_element else "No disponible"
                                isbn = self.extraer_isbn(link)
                                title = element.query_selector("h2.woocommerce-loop-product__title").inner_text().strip()
                                product_data = {
                                    "isbn": isbn,
                                    "titulo": title,
                                    "Autor": 'Template',
                                    "precio": price,
                                    "link": link,
                                    "categoria":self.categoria
                                }
                                products.append(product_data)
                            except Exception as e:
                                error_logs('flujo principal de scrap',e)
                                continue
                        
                        process_logs(f"✅ Página procesada. Total de productos acumulados: {len(products)}")
                        
                        next_page = self.pasar_pagina(page)
                        if(next_page):
                            page.wait_for_selector(".products", state="visible", timeout=60000)
                            espera = random.randint(5, 15)
                            process_logs(f"⏳ Esperando {espera} segundos antes de continuar a la siguiente pagina...")
                            time.sleep(espera)
                        else:
                            process_logs("ℹ️ Ya estamos en la última página o el enlace no es válido.")
                            break    
                    except Exception as e:
                        error_logs(f'Error en el bucle principal de scrap',e)
                        break
            except Exception as e:
                error_logs('error inicializando el navegador', e)
            finally:
                browser.close()
                self.export_to_csv(products)


