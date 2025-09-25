from .scrapStrategy import ScrapStrategy # verificar para produccion
from logic.logs import error_logs, process_logs # verificar para produccion
from class_products.book import BookProduct
from selenium.webdriver.common.by import By
import random
import time
import re
from datetime import datetime

class Buscalibre(ScrapStrategy):

    def get_selectors(self): #aqui defino los selectores para cada propiedad de producto
        return {
            'product_container': ".productos.pais42",
            'product_item': ".box-producto.producto",
            'isbn': 'data-isbn',
            'link': "a",
            'price': "strong",
            'other-price': "del",
            'title': ".nombre",
            'author': ".autor",
            'tapa': ".metas"
        }
    
    def next_page(self,sb):
        try:
            sb.wait_for_element("#pagn", timeout=10)
            next_page = sb.find_elements(".box-producto")
            if next_page:
                next_link = sb.find_elements("#pagnNextLink")
                next_href = next_link[0].get_attribute("href")
                if next_href and next_href != sb.get_current_url():
                    process_logs(f"➡️ Avanzando a la siguiente página: {next_href}")
                    sb.open(next_href)
                    sb.wait_for_ready_state_complete()
                    # Espera aleatoria para evitar ban
                    espera = random.randint(5, 15)
                    process_logs(f"⏳ Esperando {espera} segundos antes de continuar...")
                    time.sleep(espera)
                    return True
                else:
                    process_logs("ℹ️ Ya estamos en la última página o el enlace no es válido.")
                    return False
            else:
                process_logs("ℹ️ No se encontró enlace a la siguiente página. Fin de la paginación.")
                return False
        except Exception as err:
            error_logs("❌ Error al intentar avanzar a la siguiente página", str(err))
            return False
    
    def cleanIsbn(self,isbn):
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
    def get_products(self, sb, categoria):
        current_time = datetime.now().strftime('%d-%m-%Y %H:%M')
        lista_productos = []
        selectors = self.get_selectors()
        productos = sb.find_elements(selectors['product_item'])
        if productos: # IF SOLO EN DEV
            process_logs('se encontraron los productos en buscalibre strategy')
        else:
            process_logs('no se encontraron productos en buscalibre strategy')
        for producto in productos:
            try:
                isbn = producto.get_attribute(selectors['isbn'])
                titulo = producto.find_element(By.CSS_SELECTOR, selectors['title']).text.strip()
                autor = producto.find_element(By.CSS_SELECTOR, selectors['author']).text.strip()
                tapa = producto.find_element(By.CSS_SELECTOR, selectors['tapa']).text.strip()
                link = producto.find_element(By.CSS_SELECTOR, selectors['link']).get_attribute("href")
                precio_element = producto.find_element(By.CSS_SELECTOR, selectors['price'])
                
                if precio_element:
                    precio_crudo = precio_element.text.strip()
                    precio =  self.cleanPrice(precio_crudo)
                else:
                    # Buscar precio alternativo
                    try:
                        precio_element = producto.find_element(By.CSS_SELECTOR, selectors['other-price'])
                        precio_crudo = precio_element.text.strip()
                        precio = self.cleanPrice(precio_crudo)
                        if not precio:
                            process_logs('precio no disponible')
                    except:
                        precio = "Precio no disponible"
            except ValueError as err:
                error_logs('🔴 Error al obtener datos del producto', str(err))
            product = BookProduct(
                    ISBN=isbn,
                    Titulo=titulo,
                    Autor=autor,
                    Precio=precio,
                    PrecioTarjeta='Template',
                    Link=link,
                    Portada='Template',  # Debes definir esta variable
                    Editorial='Template',
                    Categoria = categoria,    # Debes definir esta variable
                    Tienda='BuscaLibre',
                    fechaScrap=current_time  # Debes definir esta variable
                )

            if product:
                lista_productos.append(product)
        
        return lista_productos if lista_productos else []
    
        