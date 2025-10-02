import os
from logic.logs import error_logs, process_logs
import csv

def csv_forAll(output_dir, nombre_csv_final):
    """
    Combina todos los archivos CSV en un directorio en un solo archivo
    
    Args:
        output_dir (str): Directorio donde están los archivos CSV
        nombre_csv_final (str): Nombre del archivo final consolidado
    """
    process_logs('✅ Iniciando proceso csv_forAll')
    
    try:
        archivos = [f for f in os.listdir(output_dir) 
                   if f.endswith('.csv') and f != nombre_csv_final]

        if not archivos:
            process_logs(f'❌ No se encontraron archivos CSV en {output_dir} (excluyendo {nombre_csv_final})')
            return False

        cabecera = None
        filas = []
        ruta_final = os.path.join(output_dir, nombre_csv_final)

        if os.path.exists(ruta_final):
            try:
                os.remove(ruta_final)
                process_logs(f"✅ Archivo existente {nombre_csv_final} eliminado.")
            except Exception as e:
                error_logs(f"❌ Error al eliminar {nombre_csv_final}: {str(e)}")
                return False

        for archivo in archivos:
            ruta_archivo = os.path.join(output_dir, archivo)
            try:
                with open(ruta_archivo, 'r', newline='', encoding='utf-8') as f:
                    lector = csv.reader(f)
                    try:
                        cabecera_archivo = next(lector)
                    except StopIteration:
                        process_logs(f"📝 {archivo} está vacío. Se omitirá.")
                        continue  

                    if cabecera is None:
                        cabecera = cabecera_archivo
                    elif cabecera != cabecera_archivo:
                        process_logs(f"⚠️ Cabecera diferente en {archivo}. Se omite.")
                        continue

                    filas_archivo = list(lector)
                    filas.extend(filas_archivo)
                    process_logs(f"✅ {archivo} procesado: {len(filas_archivo)} filas")
                    
            except Exception as e:
                error_logs(f"❌ Error en {archivo}: {str(e)}")
                continue

        if cabecera and filas:
            with open(ruta_final, 'w', newline='', encoding='utf-8') as f:
                escritor = csv.writer(f)
                escritor.writerow(cabecera)
                escritor.writerows(filas)
            process_logs(f"✅ {nombre_csv_final} creado con {len(filas)} filas de {len(archivos)} archivos")
            return True
        else:
            process_logs("❌ No hay datos válidos para crear el archivo final")
            return False
            
    except Exception as e:
        error_logs(f"❌ Error crítico en csv_forAll: {str(e)}")
        return False