import pika
import json
import atexit
import logging
from os import getenv
from dotenv import load_dotenv
import uuid


load_dotenv()
logger = logging.getLogger("app")

# Global variable to hold RabbitMQ connection and channel
connection = None
channel = None

def connect_to_rabbitmq():
    global connection, channel
    try:
        if not connection or connection.is_closed:
            params = pika.URLParameters(getenv("RABBITMQ_URL"))
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            channel.exchange_declare(exchange='user_exchange', exchange_type='fanout')
            channel.queue_declare(queue="user_activity", durable=True)
            channel.queue_bind(exchange="user_exchange", queue="user_activity")
            logger.info("Connected to RabbitMQ and declared exchange 'user_exchange' and queue 'user_activity'.")
    except Exception as e:
        logger.error(f"Error connecting to RabbitMQ: {e}")
        connection = None
        channel = None

def publish_message(message):
    global connection, channel
    try:
        if not connection or connection.is_closed or not channel or channel.is_closed:
            connect_to_rabbitmq()

        if connection and channel:
            message_id = str(uuid.uuid4())
            message_msg = {
                "message_id": message_id,
                "message": message
            }

            channel.basic_publish(
                exchange="user_exchange",
                routing_key="user_activity",
                body=json.dumps(message_msg),
                properties=pika.BasicProperties(delivery_mode=2)  # Persistent message
            )
            logger.info(f"[x] RabbitMQ message sent: {message_msg}, message_id: {message_id}")
        else:
            logger.error("Unable to send message because RabbitMQ connection is not established.")
    except Exception as e:
        logger.error(f"Error publishing message to RabbitMQ: {e}")
    finally:
        if connection and connection.is_open:
            connection.close()
            logger.info("RabbitMQ connection closed.")
    

# Ensure RabbitMQ connection closes when the application exits
atexit.register(lambda: connection.close() if connection and connection.is_open else None)
