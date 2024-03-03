import pika
import json
from mongoengine import connect
from models import Contact

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
channel = connection.channel()

# Створення черги для прийому повідомлень
channel.queue_declare(queue='email_queue', durable=True)

# Підключення до MongoDB
connect(db='My_homework_DB', host="mongodb+srv://web_8MHW:oulGmMDL5ksPq6fz@hedgehog.rsn29se.mongodb.net/My_homework_DB?retryWrites=true&w=majority&appName=hedgehog")

def callback(ch, method, properties, body):
    data = json.loads(body)
    contact_id = data['contact_id']
    contact = Contact.objects(id=contact_id).first()
    if contact:
        # Fake-надсилання повідомлення по електронній пошті та оновлення логічного поля у базі даних
        print(f"Надсилання повідомлення до {contact.email}")
        contact.message_sent = True
        contact.save()
        print(f"Повідомлення надіслано на адресу {contact.email}")


# Вказуємо, що callback буде обробляти повідомлення з черги 'email_queue'
channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print('Чекаємо на повідомлення. Якщо вихід натисність CTRL+C')
channel.start_consuming()