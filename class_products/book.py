class BookProduct():
    def __init__(self, ISBN, Titulo, Autor, Precio, Link, Portada, Editorial, Categoria, Tienda, fechaScrap): #la estregia esperada es del tipo ScrapStrategy
        self.ISBN = ISBN
        self.Titulo = Titulo
        self.Autor = Autor
        self.Precio = Precio  # aqui va la estrategia especifica
        self.Link = Link
        self.Portada = Portada  # Pasamos la categoría a la estrategia
        self.Editorial =  Editorial
        self.categoria = Categoria
        self.Tienda = Tienda
        self.fechaScrap = fechaScrap
