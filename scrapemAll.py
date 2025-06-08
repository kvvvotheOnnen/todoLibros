from scrap import Scrap

categorias = [
    ('https://www.antartica.cl/libros/arte-y-arquitectura.html', 'Arte y Arquitectura'),
    ('https://www.antartica.cl/libros/ciencias.html', 'Ciencias'),
    ('https://www.antartica.cl/libros/ciencias-exactas.html','Ciencias Exactas'),
    ('https://www.antartica.cl/libros/computacion-e-informacion.html','Computacion e informatica'),
    ('https://www.antartica.cl/libros/cuerpo-y-mente.html','Cuerpo y mente'),
    ('https://www.antartica.cl/libros/economia-y-administracion.html','Economia y administracion'),
    ('https://www.antartica.cl/libros/entretencion-y-manual.html','Entretencion y manualidades'),
    ('https://www.antartica.cl/libros/gastronomia-y-vinos.html','Gastronomia y vinos'),
    ('https://www.antartica.cl/libros/guias-de-viaje-y-tur.html','Guias de viaje y turismo'),
    ('https://www.antartica.cl/libros/infantil-y-juvenil.html','Infantil y juvenil'),
    ('https://www.antartica.cl/libros/literatura.html','Literatura'),
    ('https://www.antartica.cl/libros/mundo-comic.html','Mundo comic'),
    ('https://www.antartica.cl/libros/referencias.html','Referencias')
]

for url, categoria in categorias:
    scraper = Scrap(url, categoria)
    scraper.scrap()  
