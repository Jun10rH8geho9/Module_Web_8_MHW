import pika
import json
from models import Contact

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
channel = connection.channel()

# Створення черги для прийому повідомлень по SMS
channel.queue_declare(queue='sms_queue', durable=True)

def callback(ch, method, properties, body):
    data = json.loads(body)
    contact_id = data['contact_id']
    contact = Contact.objects(id=contact_id).first()
    if contact and contact.preferred_contact_method == "sms":
        print(f"Надсилання SMS to {contact.phone_number}")
        # Код для надсилання SMS
        contact.message_sent = True
        contact.save()
        print(f"SMS надіслано до {contact.phone_number}")

channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)

print('Чекаємо на повідомлення. Якщо вихід натисність CTRL+C')
channel.start_consuming()