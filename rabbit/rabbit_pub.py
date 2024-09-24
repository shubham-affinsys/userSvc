# users_service/rabbitmq.py
import pika
import json
import uuid

def publish_request_for_users():
    params = pika.URLParameters("amqps://sjqnwwmv:32FMj2zVoG-3U37PuWFth7nWJIu7cRuw@puffin.rmq2.cloudamqp.com/sjqnwwmv")
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    
    channel.exchange_declare(exchange='user_requests', exchange_type='fanout')
    
    message_id = str(uuid.uuid4())
    message = {
        "message_id": message_id,
        "event": "get_all_users",
    }
    
    channel.basic_publish(exchange='user_requests', routing_key='', body=json.dumps(message))
    connection.close()
    
    return message_id  # Return the message_id for tracking purposes
