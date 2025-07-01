import re
import time
import random
from logs.logs import error_logs, process_logs
import os
import csv
from seleniumbase import SB
from selenium.webdriver.common.by import By


class Scrap():
    def __init__(self, url, categoria):
        self.url = url
        self.categoria = categoria
        self.output_dir = os.getenv('OUTPUT_DIR', './data') 
        os.makedirs(self.output_dir, exist_ok=True)

    def export_to_csv(self, products):
        try:
            filename = os.path.join(self.output_dir, f"{self.categoria.replace(' ', '_')}.csv")
            file_exists = os.path.isfile(filename)

            with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['isbn', 'titulo', 'autor', 'tapa', 'precio', 'link', 'categoria']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if not file_exists:
                    writer.writeheader()

                for product in products:
                    product_data = product.copy()
                    writer.writerow(product_data)

            if os.path.exists(filename):
                process_logs(f"Archivo cvs creado exitosamente: {filename}")
                process_logs(f"📊 Total de registros guardados: {len(products)}")
                return filename
            else:
                error_logs('El archivo CSV no se creó correctamente', '')
                return None

        except Exception as err:  
            error_logs('Error en export_to_csv', str(err))
        return None

    def siguiente_pagina(self, sb):
        try:
            sb.wait_for_element("#pagn", timeout=10)
            next_link = sb.find_elements("#pagnNextLink")
            if next_link:
                next_href = next_link[0].get_attribute("href")
                if next_href and next_href != sb.get_current_url():
                    process_logs(f"➡️ Avanzando a la siguiente página: {next_href}")
                    sb.open(next_href)
                    sb.wait_for_ready_state_complete()
                    # Espera aleatoria para evitar baneos
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

    def scrap(self):
        with SB(uc=True, xvfb=True) as sb:
            lista_productos = []
            sb.uc_open(self.url)
            max_attempts = 3
            while True:
                for attempt in range(max_attempts):
                    try:
                        sb.wait_for_element(".productos.pais42")
                        break
                    except ValueError as err:
                        error_logs(f'🔴 Intento {attempt + 1}/{max_attempts} - En espera de contenedor de productos', str(err))
                        if attempt < max_attempts - 1:
                            sb.refresh_page()
                        else:
                            error_logs('❌ Conexión perdida después de 3 intentos', '')
                            if lista_productos:
                                self.export_to_csv(lista_productos)
                                process_logs(f'📊 Total de productos procesados: {len(lista_productos)}')
                            else:
                                error_logs('❌ No hay productos para exportar', '')
                            return lista_productos if lista_productos else None
                productos = sb.find_elements(".box-producto.producto")
                if not productos:
                    error_logs('❌ No se encontraron productos', '')
                    if lista_productos:
                        self.export_to_csv(lista_productos)
                        process_logs(f'📊 Total de productos procesados: {len(lista_productos)}')
                    else:
                        error_logs('❌ No hay productos para exportar', '')
                    return lista_productos if lista_productos else None
                productos_en_pagina = 0
                for producto in productos:
                    try:
                        isbn = producto.get_attribute("data-isbn")
                        titulo = producto.find_element(By.CSS_SELECTOR, ".nombre").text.strip()
                        autor = producto.find_element(By.CSS_SELECTOR, ".autor").text.strip()
                        tapa = producto.find_element(By.CSS_SELECTOR, ".metas").text.strip()
                        link = producto.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                        
                        precio_element = producto.find_element(By.CSS_SELECTOR, "strong")
                        if precio_element:
                            precio = precio_element.text.strip()
                        else:
                            precio_element = producto.find_element(By.CSS_SELECTOR, "del")
                            precio = precio_element.text.strip() if precio_element else "Precio no disponible"
                    except ValueError as err:
                        error_logs('🔴 Error al obtener datos del producto', str(err))
                    data_producto  = {
                        "isbn": isbn,
                        "titulo": titulo,
                        "autor": autor,
                        "tapa": tapa,
                        "precio": precio,
                        "link": link,
                        "categoria": self.categoria
                    }
                    if data_producto:
                        lista_productos.append(data_producto)
                        productos_en_pagina += 1
                    else:
                        error_logs('❌ Producto no agregado a la lista', '')
                process_logs(f'🔎 Total de productos encontrados en esta página: {productos_en_pagina}')
                if not self.siguiente_pagina(sb):
                    break
            if lista_productos:
                self.export_to_csv(lista_productos)
                process_logs(f'📊 Total de productos procesados: {len(lista_productos)}')
            else:
                error_logs('❌ No hay productos para exportar', '')
            return lista_productos
                    
            

