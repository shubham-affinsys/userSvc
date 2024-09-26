import pika
import json
import logging
from os import getenv
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("app")


def process_user_creation(message):
    """
    Process the message for user creation.
    Here you can add the code to create a user in your database based on the message.
    """
    try:
        user_data = json.loads(message)
        print(f"Processing user creation: {user_data}")

    except Exception as e:
        print(f"Error processing user creation: {e}")


def callback(ch, method, properties, body):
    """
    Callback function to handle the message received from RabbitMQ
    """
    print(f"Received message from RabbitMQ: {body}")
    process_user_creation(body)  # Call user creation function with the received message
    print("user created success ack the message")
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge the message


def start_subscriber():
    """
    Set up the RabbitMQ subscriber that listens for new user creation events
    """
    try:
        params = pika.URLParameters(getenv("RABBITMQ_URL"))
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        # Declare exchange and queue in case they are not already declared
        channel.exchange_declare(exchange='user_exchange', exchange_type='fanout')
        channel.queue_declare(queue="user_activity", durable=True)
        channel.queue_bind(exchange="user_exchange", queue="user_activity")

        # Start consuming messages from the queue
        channel.basic_consume(queue="user_activity", on_message_callback=callback)

        print("Subscriber started, waiting for messages.")
        channel.start_consuming()
    except Exception as e:
        print(f"Error starting RabbitMQ subscriber: {e}")