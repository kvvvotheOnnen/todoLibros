from rabbitmq_handler import RabbitMQHandler
import pytz
import datetime
from logic.logs import error_logs, process_logs
def on_csv_generated(csv_path, service_name):
    try:
        with RabbitMQHandler() as rabbit:  # Conexión automática
            chile_tz = pytz.timezone("America/Santiago")
            timestamp = datetime.now(chile_tz).strftime("%d-%m-%Y %H:%M:%S")
            rabbit.send_csv_notification(
                service_name=service_name,
                csv_path=csv_path,
                timestamp=timestamp
            )
    except Exception as e:
        error_logs(f"Error en on_csv_generated: {str(e)}")  