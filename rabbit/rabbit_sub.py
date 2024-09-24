# users_service/consumer.py
import pika
import requests
import json

def callback(ch, method, properties, body):
    message = json.loads(body)
    if message.get("event") == "get_all_users":
        try:
            response = requests.get("https://user-svc.vercel.app/users/")
            response.raise_for_status()
            data = response.json()
            # Send back the data as a response, potentially using another exchange
            print(f"Users data: {data}")  # For demo purposes, you could publish this to another queue
        except requests.exceptions.RequestException as req_err:
            print(f"Error fetching users: {req_err}")

def consume_user_requests():
    params = pika.URLParameters("amqps://sjqnwwmv:32FMj2zVoG-3U37PuWFth7nWJIu7cRuw@puffin.rmq2.cloudamqp.com/sjqnwwmv")
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    
    channel.exchange_declare(exchange='user_requests', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)  # Create a temporary queue
    queue_name = result.method.queue
    
    channel.queue_bind(exchange='user_requests', queue=queue_name)
    
    print('Waiting for user request messages.')
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    
    channel.start_consuming()
