import os
from logs_templates.logs import error_logs, process_logs
import csv
def csv_forAll(Scrap, nombre_csv_final):
        # Obtener todos los archivos CSV excepto el archivo final
        archivos = [f for f in os.listdir(Scrap.output_dir) 
                   if f.endswith('.csv') and f != nombre_csv_final]

        if not archivos:
            process_logs(f'❌No se encontraron archivos CSV en {Scrap.output_dir} (excluyendo {nombre_csv_final})')
            return False

        cabecera = None
        filas = []
        ruta_final = os.path.join(os.path.dirname(__file__), 'data')

        # Eliminar el archivo final si ya existe para empezar desde cero
        if os.path.exists(ruta_final):
            try:
                os.remove(ruta_final)
                process_logs(f"✅Archivo existente {nombre_csv_final} eliminado para crear uno nuevo.")
            except Exception as e:
                error_logs(f"❌Error al eliminar el archivo existente {nombre_csv_final}: ",{str(e)})
                return False

        for archivo in archivos:
            ruta_archivo = os.path.join(Scrap.output_dir, archivo)
            with open(ruta_archivo, newline='', encoding='utf-8') as f:
                lector = csv.reader(f)
                try:
                    cabecera_archivo = next(lector)
                except StopIteration:
                    process_logs(f"Archivo {archivo} está vacío. Se omitirá.")
                    continue  

                if cabecera is None:
                    cabecera = cabecera_archivo
                elif cabecera != cabecera_archivo:
                    process_logs(f"Advertencia: la cabecera de {archivo} es diferente. Se ignorará este archivo.")
                    continue

                filas.extend(list(lector))

        # Escribir el archivo final solo si hay datos
        if cabecera and filas:
            with open(ruta_final, 'w', newline='', encoding='utf-8') as f:
                escritor = csv.writer(f)
                escritor.writerow(cabecera)
                escritor.writerows(filas)
            process_logs(f"✅Archivo {nombre_csv_final} creado exitosamente con datos de {len(archivos)} archivos.")
            return True
        else:
            process_logs("❌No se pudo crear el archivo final: no hay datos válidos.")
            return False