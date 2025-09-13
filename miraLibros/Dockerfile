FROM mcr.microsoft.com/playwright/python:v1.52.0-noble

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt


COPY . .

RUN mkdir -p /app/data

ENV OUTPUT_DIR=/app/data
ENV LOG_DIR=/app/logs

CMD ["python3", "scrapEmAll.py"]