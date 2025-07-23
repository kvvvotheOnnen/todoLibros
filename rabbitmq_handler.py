import pika
import os
import json
import time
from dotenv import load_dotenv
from logs.logs import process_logs, error_logs

load_dotenv()

class RabbitMQHandler:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.queue_name = "cola_generacion_csv"
        self.host = os.getenv('RABBITMQ_HOST', 'rabbitmq')  # Usará el nombre del servicio
        self.port = int(os.getenv('RABBITMQ_PORT', 5672))
        self.user = os.getenv('RABBITMQ_USER')
        self.password = os.getenv('RABBITMQ_PASSWORD')
        self.max_retries = 5
        self.retry_delay = 3
    
    def connect(self):
        retries = 0
        while retries < self.max_retries:
            try:
                credentials = pika.PlainCredentials(self.user, self.password)
                parameters = pika.ConnectionParameters(
                    host=self.host,
                    port=self.port,
                    credentials=credentials,
                    heartbeat=600,
                    connection_attempts=3,
                    retry_delay=5,
                    socket_timeout=10
                )
                self.connection = pika.BlockingConnection(parameters)
                self.channel = self.connection.channel()
                
                self.channel.queue_declare(
                    queue=self.queue_name,
                    durable=True,
                    arguments={
                        'x-max-priority': 3
                    }
                )
                process_logs("✅ Conexión establecida con RabbitMQ")
                return True
                
            except Exception as e:
                retries += 1
                error_logs(f"Error connecting to RabbitMQ (attempt {retries}/{self.max_retries}): {str(e)}")
                if retries < self.max_retries:
                    time.sleep(self.retry_delay)
        
        error_logs("❌ No se pudo conectar a RabbitMQ después de varios intentos")
        return False

    def ensure_connection(self):
        if not self.connection or self.connection.is_closed:
            return self.connect()
        return True

    def send_csv_notification(self, service_name, csv_path, timestamp):
        """Envía notificación de CSV generado a la cola"""
        if not self.ensure_connection():
            error_logs("No se pudo establecer conexión con RabbitMQ")
            return False
            
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
                    delivery_mode=2,
                    content_type='application/json',
                    priority=2  # Prioridad media por defecto
                )
            )
            process_logs(f'✅ Mensaje enviado a la cola correctamente - Servicio: {service_name}')
            return True
            
        except pika.exceptions.AMQPError as e:
            error_logs(f'RabbitMQ Error - Servicio: {service_name}', f'Error al publicar mensaje: {str(e)}')
            # Intenta reconectar una vez
            if self.connect():
                return self.send_csv_notification(service_name, csv_path, timestamp)
            return False
        except Exception as e:
            error_logs(f'System Error - Servicio: {service_name}', f'Error inesperado: {str(e)}')
            return False

    def close_connection(self):
        try:
            if self.connection and self.connection.is_open:
                self.connection.close()
                process_logs("Conexión con RabbitMQ cerrada correctamente")
        except Exception as e:
            error_logs(f"Error al cerrar conexión con RabbitMQ: {str(e)}")