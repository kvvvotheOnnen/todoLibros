from .scrapStrategy import ScrapStrategy # verificar para produccion
from logic.logs import error_logs, process_logs # verificar para produccion
from class_products.book import BookProduct
import random
import time
import re
from datetime import datetime


class feriaChilena(ScrapStrategy):
    def get_selectors(self):
        return {
            'product_container': ".ast-woocommerce-container",
            'product_item': "li.ast-col-sm-12.ast-article-post.product.type-product.has-post-thumbnail",
            'link': "a.ast-loop-product__link",
            'price': "span.price .woocommerce-Price-amount",
            'title': "h2.woocommerce-loop-product__title",
            'author': ".author-selector",  
        }
    
    def cleanPrice(self, price_text):
        cleaned_price = price_text.replace("$", "").replace(".", "").strip()
        try:
            return int(cleaned_price)
        except ValueError:
            return None
    def extraer_isbn(self,url):
        match = re.search(r"/(\d+)-", url)
        if match:
            return match.group(1)  
        return None  
    def next_page(self,page):
        next_btn = page.query_selector('a.next.page-numbers')
        if not next_btn:
            return False
        next_btn.click()
        page.wait_for_selector('li.product')  
        return True
    
    def get_products(self, page, categoria):
        current_time = datetime.now().strftime('%d-%m-%Y %H:%M')
        products = []
        selectors = self.get_selectors()
        page.wait_for_selector(selectors['product_container'], state="visible", timeout=60000)
        while True:
            try:
                product_elements = page.query_selector_all(selectors['product_item'])
                process_logs(f"📚 Procesando {len(product_elements)} productos en la página actual")
                for element in product_elements:
                    try:
                        link_element = element.query_selector(selectors['link'])
                        link = link_element.get_attribute('href') if link_element else None
                        price_element = element.query_selector(selectors['price'])
                        raw_price = price_element.inner_text().strip() if price_element else "No disponible"
                        price = self.cleanPrice(raw_price) if raw_price != "No disponible" else raw_price
                        title_element = element.query_selector(selectors['title'])
                        title = title_element.inner_text().strip() if title_element else None
                        isbn = self.extraer_isbn(link) if link else "Template"

                        product = BookProduct(
                            ISBN=isbn,
                            Titulo=title,
                            Autor='Template', 
                            Precio=price,
                            Link=link,
                            Portada='Template',  
                            Editorial='Template',  
                            Categoria=categoria,
                            Tienda='feriaChilena',  
                            fechaScrap=current_time
                        )
                        products.append(product)
                    except Exception as e:
                        error_logs('Error procesando producto individual', e)
                        continue             
                process_logs(f"✅ Página procesada. Total de productos acumulados: {len(products)}")
            except Exception as e:
                error_logs('Error en el flujo principal de scrap', e)
                break
            
            return products if products else []
