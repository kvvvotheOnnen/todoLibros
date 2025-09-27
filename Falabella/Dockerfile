FROM seleniumbase:1.0

WORKDIR /app
RUN pip install --no-cache-dir pika python-dotenv pytz selenium

COPY . .




CMD ["python3", "scrapEmAll.py"]
