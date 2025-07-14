import pika
import os
import json
from dotenv import load_dotenv
from logs.logs import process_logs, error_logs

load_dotenv()

class RabbitMQHandler:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.queue_name = "cola_generacion_csv"  # Nombre de la cola única
        self.host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
        self.port = int(os.getenv('RABBITMQ_AMQP_PORT', 5672))
        self.user = os.getenv('RABBITMQ_DEFAULT_USER')
        self.password = os.getenv('RABBITMQ_DEFAULT_PASS')
    
    def connect(self):
        try:
            credentials = pika.PlainCredentials(self.user, self.password)
            parameters = pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=credentials,
                heartbeat=600  # Mantener conexión activa
            )
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # declara cola unica
            self.channel.queue_declare(
                queue=self.queue_name,
                durable=True,  # para los reinicios
                arguments={
                    'x-max-priority': 3  # proriedad del 1 al 3 por si hace falta 
                }
            )
            return True
        except Exception as e:
            print(f"Error connecting to RabbitMQ: {str(e)}")
            return False
    
    def send_csv_notification(self, service_name, csv_path, timestamp):
        """Envía notificación de CSV generado a la cola única"""
        message = {
            "event_type": "csv_generated",
            "service": service_name,
            "csv_path": csv_path,
            "timestamp": timestamp,
            "status": "success"
        }
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # mensaje persistente para los reinicios
                    content_type='application/json'
                )
            )
            return True
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            return False
    
    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()