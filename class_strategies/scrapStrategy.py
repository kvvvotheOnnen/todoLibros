from abc import ABC, abstractmethod

class ScrapStrategy(ABC):
    @abstractmethod
    def next_page(self, page):
        pass
    
    @abstractmethod
    def get_products(self, page):
        pass
    
    @abstractmethod
    def get_selectors(self):
        #aca devolvemos los selectores especificos por pagina
        pass
    @abstractmethod
    def update_products_isbn(self, page, product_list):
        """Actualiza los ISBNs de los productos (opcional)"""
        # Por defecto no hace nada, las estrategias que lo necesiten lo implementarán
        return product_list

