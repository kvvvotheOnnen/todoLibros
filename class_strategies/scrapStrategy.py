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

