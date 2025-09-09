from logs_templates.logs import error_logs, process_logs # verificar para produccion
def scrapEmAll(categorias, Scrap):
    products = []
    for url in categorias:
        process_logs(f"Llegamos a {url},⏳ Esperando {espera} segundos antes de continuar")
        categories = Scrap(url, url[1])
