from .scrapStrategy import ScrapStrategy # verificar para produccion
from logic.logs import error_logs, process_logs # verificar para produccion
from class_products.book import BookProduct
import random
import time
import re
from datetime import datetime


class MiraLibros(ScrapStrategy):
    def get_selectors(self): #aqui defino los selectores para cada propiedad de producto
        return {
            'product_container': ".col-lg-12.col-md-12",
            'product_item': ".product-block",
            'link': "a",
            'price': ".block-price",
            'title': "h3 a",
            'isbn':'span.sku_elem"'
        }
    
    def needs_isbn_update(self): #esto lo reescribimos despues en el scrap
        return True  # por defecto no necesita
    

    def update_products_isbn(self, browser, product_list):  # Cambia page por browser
        """Actualiza los ISBNs de todos los productos en la lista"""
        for i, product in enumerate(product_list, 1):
            try:
                process_logs(f'Obteniendo ISBN {i}/{len(product_list)}: {product.Link}')
                
                if product.ISBN != 'Template':
                    continue
                    
                # Pasar el browser en lugar de la page
                isbn = self.obtener_isbn_desde_link(browser, product.Link)
                product.ISBN = isbn
                process_logs(f'✅ ISBN actualizado: {isbn}')
                
                if i < len(product_list):
                    time.sleep(random.uniform(1, 3))
                    
            except Exception as e:
                error_logs(f'❌ Error actualizando ISBN para {product.Link}', str(e))
        
        return product_list
    
    def obtener_isbn_desde_link(self, browser, product_link):  # Cambia page por browser
        """Obtiene el ISBN de un link específico"""
        try:
            if not product_link or product_link == 'Template':
                return 'Template'
                
            # Crear nuevo contexto y página usando el browser
            context = browser.new_context()
            new_page = context.new_page()
            
            new_page.goto(product_link, wait_until='domcontentloaded', timeout=30000)
            
            # Buscar el elemento del ISBN
            isbn_selector = self.get_selectors()['isbn']
            isbn_element = new_page.wait_for_selector(isbn_selector, timeout=10000)
            
            if isbn_element:
                isbn = isbn_element.inner_text().strip()
            else:
                isbn = 'Template'
                error_logs(f'❌ No se encontró ISBN en: {product_link}')
            
            # Cerrar recursos
            new_page.close()
            context.close()
            return isbn
            
        except Exception as e:
            error_logs(f'❌ Error obteniendo ISBN de {product_link}', str(e))
            return 'Template'
        
    
    def cleanPrice(self, price_text):
        cleaned_price = price_text.replace("$", "").replace(".", "").strip()
        try:
            return int(cleaned_price)
        except ValueError:
            return None
    
    def next_page(self,page):
        next_btn = page.query_selector('a.square-button i.fas.fa-angle-right')
        if not next_btn:
            return False
        
        next_link = next_btn.query_selector('xpath=..')
        if not next_link:
            return False
        
        href = next_link.get_attribute('href')
        if not href:
            process_logs("ℹ️ Llegamos a la última página - el botón no tiene href")
            return False
        
        class_attribute = next_link.get_attribute('class')
        if class_attribute and 'disabled' in class_attribute:
            process_logs("ℹ️ Llegamos a la última página - el botón está deshabilitado")
            return False

        next_link.click()
        page.wait_for_selector('.product-block')  # Espera a que carguen los productos
        return True
     
    def get_products(self, page, categoria):
        current_time = datetime.now().strftime('%d-%m-%Y %H:%M')
        products = []
        selectors = self.get_selectors()
        product_elements = page.query_selector_all(selectors['product_item'])
        for element in product_elements:
            try:            
                link_element = element.query_selector(selectors['link'])
                rawLink = link_element.get_attribute('href') if link_element else None
                link = f'https://miralibros.cl/{rawLink}'
                price_element = element.query_selector(selectors['price'])
                rawPrice = price_element.inner_text().strip() if price_element else None
                price = self.cleanPrice(rawPrice) if rawPrice else None
                title_element = element.query_selector(selectors['title'])
                title = title_element.inner_text().strip() if link_element else None

                product = BookProduct(
                    ISBN='Template',
                    Titulo=title,
                    Autor='Template',
                    Precio=price,
                    PrecioTarjeta='Template',
                    Link=link,
                    Portada='Template',  
                    Editorial='Template',
                    Categoria = categoria,    
                    Tienda='miraLibros',
                    fechaScrap=current_time  
                )
                products.append(product)
            except Exception as e:
                error_logs('❌Miralibros: get_products', str(e))
            continue
        return products if products else []

