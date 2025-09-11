import os
import csv
from logic.logs import error_logs, process_logs

def export_to_csv(products, categoria):
    try:
        if not products:
            process_logs("⚠️ No hay productos para exportar")
            return None
        
        # Configuración de directorios
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        filename = os.path.join(data_dir, f"{categoria}.csv")
        file_exists = os.path.exists(filename)
        
        # Contar registros existentes si el archivo ya existe
        existing_count = 0
        if file_exists:
            with open(filename, 'r', encoding='utf-8') as f:
                existing_count = sum(1 for _ in f) - 1  # Restar el header
        
        fieldnames = [
            'ISBN', 'Titulo', 'Autor', 'Precio', 'Link',
            'Portada', 'Editorial', 'Categoria', 'Tienda', 'Fecha'
        ]
        
        mode = 'a' if file_exists else 'w'
        
        with open(filename, mode=mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            for product in products:
                product_dict = {
                    'ISBN': product.ISBN,
                    'Titulo': product.Titulo,
                    'Autor': product.Autor,
                    'Precio': product.Precio,
                    'Link': product.Link,
                    'Portada': product.Portada,
                    'Editorial': product.Editorial,
                    'Categoria': product.categoria,
                    'Tienda': product.Tienda,
                    'Fecha': product.fechaScrap
                }
                writer.writerow(product_dict)
        
        # Mensaje informativo
        total_records = existing_count + len(products) if file_exists else len(products)
        process_logs(f"✅ CSV {'actualizado' if file_exists else 'creado'}: {filename}")
        process_logs(f"📊 Nuevos registros: {len(products)}")
        process_logs(f"📈 Total acumulado: {total_records} registros")
        
        return filename
        
    except Exception as err:
        error_logs('❌ Error en export_to_csv', str(err))
        return None