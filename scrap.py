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
            error_logs('Error en metodo de scrap cleanIsbn', err)
    def cleanPrice(self, price_text):
        cleaned_price = price_text.replace("$", "").replace(".", "").strip()
        try:
            return int(cleaned_price)
        except ValueError:
            return None
    
    def export_to_csv(self, products):
        try:
            filename = os.path.join(self.output_dir, f"{self.categoria.replace(' ', '_')}.csv")
            file_exists = os.path.isfile(filename)

            with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['isbn', 'titulo', 'Autor', 'precio', 'link', 'categoria']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if not file_exists:
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

        except Exception as err:  # Captura todos los tipos de error, no solo ValueError
            error_logs('Error en export_to_csv', str(err))
        return None



    def scrap(self):
        products = []
        with sync_playwright() as p:
            try:
                browser = p.firefox.launch(headless=True)
                page = browser.new_page()
                page.goto(self.url)
                page.wait_for_selector(".products.list.items.product-items", state="visible", timeout=60000)
                while True:
                    try:
                        # Scrapear productos de la página actual
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
                                
                                author_element = element.query_selector(".product-item-author")
                                author = author_element.inner_text().strip() if author_element else None
                                
                                product_data = {
                                    "isbn": isbn,
                                    "titulo": title,
                                    "Autor": author,
                                    "precio": price,
                                    "link": link,
                                    "categoria":self.categoria
                                }
                                products.append(product_data)
                            except Exception as e:
                                error_logs('flujo principal de scrap',e)
                                continue
                        current_page = page.query_selector(".item.current")
                        if not current_page:
                            break

                        last_item = page.query_selector(".item.item-margin-right-0")
                        if not last_item:
                            break

                        next_item = current_page.evaluate_handle("(element) => element.nextElementSibling")
                        if not next_item:
                            break
                            
                        next_page_link = next_item.query_selector("a")
                        if not next_page_link:
                            break

                        new_url = next_page_link.get_attribute('href')
                        if not new_url:
                            break
                        delay_seconds = random.randint(5, 15)
                        time.sleep(delay_seconds)
                        process_logs(f"{self.categoria}|| Avanzando a: {new_url}, luego de una espera de {delay_seconds} segundos")
                        page.goto(new_url)
                        page.wait_for_selector(".products.list.items.product-items", state="visible", timeout=60000)

                        
                    except Exception as e:
                        error_logs(f'Error en el bucle principal de scrap',e)
                        break
            except Exception as e:
                error_logs('error inicializando el navegador', e)
            finally:
                browser.close()
                self.export_to_csv(products)


