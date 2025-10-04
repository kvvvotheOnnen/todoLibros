import os
import pika
from logic.logs import error_logs, process_logs
import time
import json
class RabbitMQHandler:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.queue_name = os.getenv('RABBITMQ_QUEUE')
        self.host = os.getenv('RABBITMQ_HOST')  
        
        port_str = os.getenv('RABBITMQ_PORT', '5672')
        try:
            self.port = int(port_str)  
        except (TypeError, ValueError):
            self.port = 5666  
            
        self.user = os.getenv('DEFAULT_USER_DEV')
        self.password = os.getenv('DEFAULT_PASS_DEV')
        self.max_retries = int(os.getenv('RABBITMQ_MAX_RETRIES', '5'))
        self.retry_delay = int(os.getenv('RABBITMQ_RETRY_DELAY', '3'))
        
        self._validate_config()
    
    def _validate_config(self):
        required_config = {
            'RABBITMQ_QUEUE': self.queue_name,
            'RABBITMQ_HOST': self.host,
            'DEFAULT_USER_DEV': self.user,
            'DEFAULT_PASS_DEV': self.password
        }
        
        missing = [key for key, value in required_config.items() if not value]
        if missing:
            raise ValueError(f"Variables de entorno faltantes: {', '.join(missing)}")
    
    def __enter__(self):
        if not self.ensure_connection():
            raise ConnectionError("No se pudo conectar a RabbitMQ")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()
        return False  
    
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
                error_logs(f"Error connecting to RabbitMQ (attempt {retries}/{self.max_retries}):", str(e))
                if retries < self.max_retries:
                    time.sleep(self.retry_delay)
        
        process_logs("❌ No se pudo conectar a RabbitMQ después de varios intentos")
        return False

    def ensure_connection(self):
        if not self.connection or self.connection.is_closed:
            return self.connect()
        return True

    def send_csv_notification(self, service_name,timestamp):
        try:
            if not self.ensure_connection():
                process_logs("RabbitMQ: No se pudo establecer conexión")
                return False

            message = {
                "event_type": "csv_generated",
                "service": service_name,
                "csv_path": f'data/{service_name}.csv',
                "timestamp": timestamp, 
                "status": "success"
            }

            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Persistente
                    content_type='application/json'
                )
            )
            process_logs(f'✅ Mensaje enviado - {service_name}')
            return True

        except pika.exceptions.AMQPError as e:
            error_logs(f'RabbitMQ Error - {service_name}', str(e))
            return False
        except Exception as e:
            error_logs(f'Error inesperado - {service_name}', str(e))
            return False

    def close_connection(self):
        try:
            if self.connection and self.connection.is_open:
                self.connection.close()
                process_logs("Conexión con RabbitMQ cerrada correctamente")
        except Exception as e:
            error_logs(f"Error al cerrar conexión con RabbitMQ:",str(e))