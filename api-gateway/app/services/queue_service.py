import json 
import pika
from app.cores.config import * 

EXCHANGE_NAME = "inference"

def publish_job(task_data):
    routing_key = task_data["task_type"]
    if routing_key is None:
        raise ValueError("job_data must include field 'type'.")
    
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=credentials
        )
    )
    channel = connection.channel()

    # Declare topic exchange
    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type="topic",
        durable=True
    )

    message = json.dumps(task_data)

    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=routing_key,
        body=message,
        # keep job persistent when rabbitmq is restart
        properties=pika.BasicProperties(delivery_mode=2)
    )

    connection.close()

    return True
