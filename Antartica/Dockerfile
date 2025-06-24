# Usa la imagen oficial de Python con la versión que necesites
FROM python:3.10-slim

# Instala dependencias del sistema para Playwright y Firefox
RUN apt-get update && \
    apt-get install -y \
    wget \
    libxtst6 \
    libxrender1 \
    libfontconfig1 \
    libdbus-glib-1-2 \
    libgtk-3-0 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Instala Playwright y los browsers necesarios
RUN pip install playwright && \
    playwright install firefox && \
    playwright install-deps

# Crea y configura el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY . .

# Instala dependencias de Python (asegúrate de tener requirements.txt)
RUN pip install -r requirements.txt

# Comando para ejecutar tu script principal
CMD ["python", "scrapemAll.py"]
