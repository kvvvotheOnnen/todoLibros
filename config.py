# config.py
import os
import sys
from pathlib import Path

def find_project_root():

    current_path = Path(__file__).resolve()
    
    # Marcadores que indican la raíz del proyecto
    root_indicators = ['.git', 'docker-compose.yml']
    
    # Buscar hacia arriba hasta encontrar un marcadosr
    for parent in [current_path] + list(current_path.parents):
        if any((parent / marker).exists() for marker in root_indicators):
            return parent
    
    # Fallback: directorio del config.py
    return current_path.parent

def setup_environment():
    """Configura el entorno automáticamente"""
    # Detectar Docker
    IS_DOCKER = os.path.exists('/.dockerenv')
    
    # Encontrar la raíz del proyecto
    if IS_DOCKER:
        print('Modo Produccion detectado')
        project_root = Path('/app')
    else:
        print('Modo desarrollo detectado')
        project_root = find_project_root()
    
    # Configurar PythonPath
    common_path = project_root / 'logic'
    
    # Agregar paths necesarios
    paths_to_add = [
        str(project_root),          # Raíz del proyecto
        str(common_path),           # Módulos comunes
    ]
    
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    print(f"Project root: {project_root}")
    print(f"PythonPath configurado: {sys.path}")
    
    return project_root

# Ejecutar al importar
PROJECT_ROOT = setup_environment()