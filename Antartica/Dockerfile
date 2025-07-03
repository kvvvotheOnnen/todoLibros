GNU nano 4.8                       Dockerfile                                 
FROM mcr.microsoft.com/playwright/python:v1.52.0-noble

WORKDIR /app

# Copia solo lo necesario primero para cachear dependencias
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código después
COPY . .

# Asegura los permisos correctos para Playwright
RUN chmod -R 777 /ms-playwright

CMD ["python", "scrapemAll.py"]
