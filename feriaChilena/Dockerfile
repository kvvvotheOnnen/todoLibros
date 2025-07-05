FROM mcr.microsoft.com/playwright:v1.40.0-jammy

# Instalar Python y pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

RUN playwright install firefox
RUN playwright install-deps firefox

COPY . .

RUN mkdir -p /app/data

ENV OUTPUT_DIR=/app/data
ENV LOG_DIR=/app/logs

CMD ["python3", "scrapEmAll.py"]