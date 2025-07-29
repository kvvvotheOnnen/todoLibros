FROM seleniumbase

WORKDIR /app
RUN pip install --no-cache-dir pika python-dotenv pytz

COPY . .




CMD ["python3", "scrapEmAll.py"]
