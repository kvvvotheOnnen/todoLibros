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
            with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['isbn', 'titulo', 'autor', 'precio', 'link', 'categoria']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
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
            sb.wait_for_element("#testId-pagination-top-arrow-right", timeout=10)
            next_btn = sb.find_element("#testId-pagination-top-arrow-right")
            is_disabled = next_btn.get_attribute("disabled")
            if is_disabled is not None:
                process_logs("ℹ️ Ya estamos en la última página o el botón está deshabilitado.")
                return False
            else:
                next_btn.click()
                sb.wait_for_ready_state_complete()
                espera = random.randint(5, 15)
                process_logs(f"⏳ Esperando {espera} segundos antes de continuar...")
                time.sleep(espera)
                return True
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
                        sb.wait_for_element("#testId-searchResults-products")
                        break
                    except Exception as err:
                        error_logs(f'🔴 Intento {attempt + 1}/{max_attempts} - En espera de contenedor de productos', str(err))
                        if attempt < max_attempts - 1:
                            sb.refresh_page()
                        else:
                            error_logs('❌ Conexión perdida después de 3 intentos', '')
                            break
                else:
                    break
                productos = sb.find_elements(".jsx-3752256814.search-results-4-grid.grid-pod")
                if not productos:
                    error_logs('❌ No se encontraron productos', '')
                    break
                productos_en_pagina = 0
                for producto in productos:
                    try:
                        isbn = "N/A"
                        try:
                            autor = producto.find_element(By.CSS_SELECTOR, "b.pod-title").text.strip()
                        except Exception:
                            autor = "N/A"
                        try:
                            titulo = producto.find_element(By.CSS_SELECTOR, "b.pod-subTitle").text.strip()
                        except Exception:
                            subtitulo = producto.find_elements(By.CSS_SELECTOR, "b[id^='testId-pod-displaySubTitle-']")
                            titulo = subtitulo[0].text.strip() if subtitulo else "N/A"
                        link = producto.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                        try:
                            precios = producto.find_elements(By.CSS_SELECTOR, "div[id^='testId-pod-prices-'] span")
                            precio = "N/A"
                            for span in precios:
                                clase = span.get_attribute("class")
                                if not clase or "crossed" not in clase:
                                    precio = span.text.strip()
                                    break
                        except Exception:
                            precio = "N/A"
                    except ValueError as err:
                        error_logs('🔴 Error al obtener datos del producto', str(err))
                    data_producto  = {
                        "isbn": isbn,
                        "titulo": titulo,
                        "autor": autor,
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
                    
    def csv_forAll(self, nombre_csv_final):
        """
        Une todos los archivos CSV de la carpeta data en uno solo, usando la cabecera del primero.
        El archivo final se guarda en la misma carpeta data con el nombre proporcionado.
        """
        archivos = [f for f in os.listdir(self.output_dir) if f.endswith('.csv')]
        if not archivos:
            process_logs(f'No se encontraron archivos CSV en {self.output_dir}')
            return

        cabecera = None
        filas = []

        for archivo in archivos:
            ruta_archivo = os.path.join(self.output_dir, archivo)
            with open(ruta_archivo, newline='', encoding='utf-8') as f:
                lector = csv.reader(f)
                try:
                    cabecera_archivo = next(lector)
                except StopIteration:
                    continue  # archivo vacío
                if cabecera is None:
                    cabecera = cabecera_archivo
                elif cabecera != cabecera_archivo:
                    process_logs(f"Advertencia: la cabecera de {archivo} es diferente. Se ignorará este archivo.")
                    continue
                filas.extend(list(lector))

        if cabecera is None:
            process_logs('No se pudo determinar la cabecera de los archivos CSV.')
            return

        ruta_final = os.path.join(self.output_dir, nombre_csv_final)
        with open(ruta_final, 'w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            escritor.writerow(cabecera)
            escritor.writerows(filas)
        process_logs(f'Se creó el archivo {ruta_final} con {len(filas)} filas.')
                    
            

