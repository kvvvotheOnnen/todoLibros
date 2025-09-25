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
        }
    
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

