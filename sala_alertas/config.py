"""Configuración de rutas del proyecto."""

from pathlib import Path

# Carpeta raíz del proyecto (donde están PROYECTO.md y CLAUDE.md)
RAIZ_PROYECTO = Path(__file__).resolve().parents[1]

# Carpeta con los archivos descargados tal cual de las fuentes
RUTA_DATOS_CRUDOS = RAIZ_PROYECTO / "datos" / "crudos"

# Carpeta con los datos generados por código
RUTA_DATOS_PROCESADOS = RAIZ_PROYECTO / "datos" / "procesados"

# Archivo de la base de datos SQLite
RUTA_BASE_DATOS = RUTA_DATOS_PROCESADOS / "sala_alertas.db"