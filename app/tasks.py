import pika
import json
import threading

def get_connection():
    return pika.BlockingConnection(pika.ConnectionParameters('localhost'))

def publish_message(queue_name, message):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()

def process_booking_notification(ch, method, properties, body):
    message = json.loads(body)
    print(f"[NOTIFICATION] Booking confirmed for {message['student_name']} with tutor {message['tutor_id']} on {message['date']} at {message['time']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def process_payment_notification(ch, method, properties, body):
    message = json.loads(body)
    print(f"[PAYMENT] Payment {message['status']} for booking {message['booking_id']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer(queue_name, callback):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    print(f"[*] Waiting for messages in {queue_name}")
    channel.start_consuming()

def start_workers():
    t1 = threading.Thread(target=start_consumer, args=('booking_notifications', process_booking_notification), daemon=True)
    t2 = threading.Thread(target=start_consumer, args=('payment_notifications', process_payment_notification), daemon=True)
    t1.start()
    t2.start()