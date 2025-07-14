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

    def cleanIsbn(self, isbn):
        try:
            texto_limpio = re.sub(r"_.*", "", isbn)
            return texto_limpio
        except ValueError as err:
            error_logs('Error en metodo de scrap cleanIsbn', str(err))
    def cleanPrice(self, price_text):
        cleaned_price = price_text.replace("$", "").replace(".", "").strip()
        try:
            return int(cleaned_price)
        except ValueError:
            return None
    
    def pasar_pagina(self,page):
        try:
            next_button =  page.query_selector('a.next-page')
            if not next_button:
                process_logs("❌ No se encuentra el boton de pasar pagina")
                return False
            href =  next_button.get_attribute('href')
            if href and (href.strip().lower() == 'javascript:void(0)' or 
                         href.strip().lower() == '#'):
                process_logs('✅ Ultima pagina ya escrapeada !')
                return False
            next_button.click()
            page.wait_for_selector('.products.list.items.product-items')
            espera = random.randint(5, 15)
            process_logs(f"Llegamos a {href},⏳ Esperando {espera} segundos antes de continuar")
            time.sleep(espera)
            return True
        except ValueError as e:
            error_logs('❌En metodo pasar pagina',{e})
            return False
    def export_to_csv(self, products):
        try:
            filename = os.path.join(self.output_dir, f"{self.categoria.replace(' ', '_')}.csv")
            with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['isbn', 'titulo', 'autor', 'precio', 'link', 'categoria']
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
                    continue  
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
                browser = p.firefox.launch(headless=False)
                page = browser.new_page()
                page.goto(self.url)
                page.wait_for_selector(".products.list.items.product-items", state="visible", timeout=60000)
                while True:
                    try:
                        product_elements = page.query_selector_all(".product-item-info")
                        for element in product_elements:
                            try:
                                rawIsbn = element.query_selector('.product-image-photo')
                                testIsbn = rawIsbn.get_attribute("alt") if rawIsbn else None
                                isbn = self.cleanIsbn(testIsbn) if testIsbn else None
                                
                                link_element = element.query_selector(".product.photo.product-item-photo")
                                link = link_element.get_attribute('href') if link_element else None
                                
                                price_element = element.query_selector(".price-wrapper")
                                rawPrice = price_element.inner_text().strip() if price_element else None
                                price = self.cleanPrice(rawPrice) if rawPrice else None
                                
                                title_element = element.query_selector(".product-item-link")
                                title = title_element.inner_text().strip() if title_element else None
                                
                                author_element = element.query_selector(".link-autor-search-result")
                                author = author_element.inner_text().strip() if author_element else None
                                
                                product_data = {
                                    "isbn": isbn,
                                    "titulo": title,
                                    "autor": author,
                                    "precio": price,
                                    "link": link,
                                    "categoria":self.categoria
                                }
                                products.append(product_data)
                            except Exception as e:
                                error_logs('flujo principal de scrap', str(e))
                                continue
                            
                        if not self.pasar_pagina(page):
                            break
                    except Exception as e:
                        error_logs(f'Error en el bucle principal de scrap', str(e))
                        break
            except Exception as e:
                error_logs('error inicializando el navegador', str(e))
            finally:
                browser.close()
                self.export_to_csv(products)


