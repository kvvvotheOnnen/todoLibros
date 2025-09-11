from .scrapStrategy import ScrapStrategy # verificar para produccion
from logic.logs import error_logs, process_logs # verificar para produccion
from class_products.book import BookProduct
import random
import time
import re
from datetime import datetime

class Antartica(ScrapStrategy):
    def get_selectors(self): #aqui defino los selectores para cada propiedad de producto
        return {
            'product_container': ".products.list.items.product-items",
            'product_item': ".product-item-info",
            'isbn': '.product-image-photo',
            'link': ".product.photo.product-item-photo",
            'price': ".price-wrapper",
            'title': ".product-item-link",
            'author': ".link-autor-search-result"
        }
    
    def next_page(self,page):
        try:
            next_button = page.query_selector('a.next-page')
            if not next_button:
                process_logs("❌ No se encuentra el boton de pasar pagina")
                return False
            
            href = next_button.get_attribute('href')
            if href and (href.strip().lower() == 'javascript:void(0)' or 
                         href.strip().lower() == '#'):
                process_logs('✅ Ultima pagina ya escrapeada !')
                return False
            
            next_button.click()
            selectors = self.get_selectors()
            page.wait_for_selector(selectors['product_container'])
            espera = random.randint(5, 15)
            process_logs(f"Llegamos a {href}")
            return True
        except ValueError as e:
            error_logs('❌En metodo pasar pagina',{e})
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
    def get_products(self, page, categoria):
        current_time = datetime.now().strftime('%d-%m-%Y %H:%M')
        products = []
        selectors = self.get_selectors()
        product_elements = page.query_selector_all(selectors['product_item'])
        for element in product_elements:
            try:
                rawIsbn = element.query_selector(selectors['isbn'])
                testIsbn = rawIsbn.get_attribute("alt") if rawIsbn else None
                isbn = self.cleanIsbn(testIsbn) if testIsbn else None
                
                link_element = element.query_selector(selectors['link'])
                link = link_element.get_attribute('href') if link_element else None
                
                price_element = element.query_selector(selectors['price'])
                rawPrice = price_element.inner_text().strip() if price_element else None
                price = self.cleanPrice(rawPrice) if rawPrice else None
                
                title_element = element.query_selector(selectors['title'])
                title = title_element.inner_text().strip() if title_element else None
                
                author_element = element.query_selector(selectors['author'])
                author = author_element.inner_text().strip() if author_element else None
                product = BookProduct(
                    ISBN=isbn,
                    Titulo=title,
                    Autor=author,
                    Precio=price,
                    Link=link,
                    Portada='Template',  # Debes definir esta variable
                    Editorial='Template',
                    Categoria = categoria,    # Debes definir esta variable
                    Tienda='Template',
                    fechaScrap=current_time  # Debes definir esta variable
                )
                products.append(product)
            except Exception as e:
                error_logs('❌Antartica: get_products', str(e))
                continue
        
        return products if products else []
    
        