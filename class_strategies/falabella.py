from .scrapStrategy import ScrapStrategy # verificar para produccion
from logic.logs import error_logs, process_logs # verificar para produccion
from class_products.book import BookProduct
from selenium.webdriver.common.by import By
import random
import time
import re
from datetime import datetime

class Falabella(ScrapStrategy):

    def get_selectors(self):
        return {
            'product_container': "#testId-searchResults-products", 
            'product_item': ".jsx-3752256814.search-results-4-grid.grid-pod",  
            'link': "a",
            'price': "[class*='primary'][class*='medium']",
            'cmr': "[class*='primary'][class*='high']",  # Precio con tarjeta cmr
            'title': "b[id^='testId-pod-displaySubTitle-']",
            'isbn':"//td[@class='jsx-960159652 property-name' and text()='ISBN']/following-sibling::td[@class='jsx-960159652 property-value']"  
        }
    def needs_isbn_update(self): #esto lo reescribimos despues en el scrap
        return True
    
    def update_products_isbn(self, sb, product_list):
        """Actualiza los ISBNs de todos los productos en la lista"""
        for i, product in enumerate(product_list, 1):
            try:
                process_logs(f'Obteniendo ISBN {i}/{len(product_list)}: {product.Link}')

                if product.ISBN != 'Template':
                    continue

                # Obtener ISBN navegando directamente
                isbn = self.obtener_isbn_desde_link(sb, product.Link)
                product.ISBN = isbn
                process_logs(f'✅ ISBN actualizado: {isbn}')

                # Espera entre requests
                if i < len(product_list):
                    waitTime = random.uniform(4, 8)
                    process_logs(f'Esperando {waitTime} segundos para el proximo isbn')
                    time.sleep(waitTime)

            except Exception as e:
                error_logs(f'❌ Error actualizando ISBN para {product.Link}', str(e))

        return product_list
    
    def obtener_isbn_desde_link(self, sb, product_link):
        """Obtiene el ISBN de un link específico usando SeleniumBase"""
        try:
            if not product_link or product_link == 'Template':
                return 'Template'

            # Navegar directamente al enlace del producto en la misma pestaña
            sb.open(product_link)

            # Buscar el elemento del ISBN
            isbn_selector = self.get_selectors()['isbn']

            # Esperar a que el elemento esté presente
            if sb.wait_for_element(isbn_selector, timeout=10):
                isbn = sb.get_text(isbn_selector).strip()
                process_logs(f'✅ ISBN encontrado: {isbn}')
            else:
                isbn = 'Template'
                error_logs(f'❌ No se encontró ISBN en: {product_link}')

            return isbn

        except Exception as e:
            error_logs(f'❌ Error obteniendo ISBN de {product_link}', str(e))
            return 'Template'
    
    
    def next_page(self,sb):
        try:
            sb.wait_for_element("#testId-pagination-top-arrow-right", timeout=10)
            next_btn = sb.find_element("#testId-pagination-top-arrow-right")
            is_disabled = next_btn.get_attribute("disabled")
            if is_disabled is not None:
                process_logs("ℹ️ Ya estamos en la última página o el botón está deshabilitado.")
                return False
            else:
                next_btn.click()
                sb.wait_for_ready_state_complete()
                espera = random.randint(5, 15)
                process_logs(f"⏳ Esperando {espera} segundos antes de continuar...")
                time.sleep(espera)
                return True
        except Exception as err:
            error_msg = str(err)
            if "element click intercepted" in error_msg:
                if "kampyleInviteContainer" in error_msg:
                    process_logs("🚫 Popup detectado: kampyleInviteContainer interceptando clic")
                else:
                    process_logs("🚫 Elemento interceptando clic (footer u otro elemento)")
                sb.refresh_page()
                time.sleep(3)  #Temporizador
                return True
            else:    
                error_logs("❌ Error al intentar avanzar a la siguiente página", str(err))
                return False
    
    def cleanIsbn(self,isbn):
        try:
            texto_limpio = re.sub(r"_.*", "", isbn)
            return texto_limpio
        except ValueError as err:
            error_logs('Error en metodo de scrap cleanIsbn', str(err))
    
    #Metodo unico de falabella para limpiar links
    def clean_url(self, url):
        return url.split('?')[0] if url and url != "N/A" else url
    
    def cleanPrice(self, price_text):
        cleaned_price = price_text.replace("$", "").replace(".", "").strip()
        try:
            return int(cleaned_price)
        except ValueError:
            return None
    def get_products(self, sb, categoria):
        current_time = datetime.now().strftime('%d-%m-%Y %H:%M')
        lista_productos = []
        selectors = self.get_selectors()
        productos = sb.find_elements(selectors['product_item'])
        if productos: # IF SOLO EN DEV
            process_logs('se encontraron los productos en Falabella strategy')
        else:
            process_logs('no se encontraron productos en Falabella strategy')
        for producto in productos:
            try:
                titulo = producto.find_element(By.CSS_SELECTOR, selectors['title']).text.strip()
                rawLink = producto.find_element(By.CSS_SELECTOR, selectors['link']).get_attribute("href")
                link = self.clean_url(rawLink)
                try:
                    precio_element = producto.find_element(By.CSS_SELECTOR, selectors['cmr']).text.strip()
                    precioTarjeta =  self.cleanPrice(precio_element)
                    rawAlterPrice = producto.find_element(By.CSS_SELECTOR, selectors['price'])
                    alterPrice = self.cleanPrice(rawAlterPrice)

                except:
                    rawAlterPrice = producto.find_element(By.CSS_SELECTOR, selectors['price']).text.strip()
                    alterPrice = self.cleanPrice(rawAlterPrice)
                    precioTarjeta = 'Template'
            except ValueError as err:
                error_logs('🔴 Error al obtener datos del producto', str(err))
            product = BookProduct(
                    ISBN='Template',
                    Titulo=titulo,
                    Autor='Template',
                    Precio=alterPrice,
                    PrecioTarjeta=precioTarjeta,
                    Link=link,
                    Portada='Template', 
                    Editorial='Template',
                    Categoria = categoria,   
                    Tienda='Falabella',
                    fechaScrap=current_time  
                )

            if product:
                lista_productos.append(product)
        
        return lista_productos if lista_productos else []
    
        