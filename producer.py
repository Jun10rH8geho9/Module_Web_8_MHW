import pika
import json
from mongoengine import connect
from models import Contact
from faker import Faker
from bson import ObjectId

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
channel = connection.channel()

# Створення черги для відправки повідомлень для email
channel.queue_declare(queue='email_queue', durable=True)

# Створення черги для відправки повідомлень для SMS
channel.queue_declare(queue='sms_queue', durable=True)


# Підключення до MongoDB
connect(db='My_homework_DB', host="mongodb+srv://web_8MHW:oulGmMDL5ksPq6fz@hedgehog.rsn29se.mongodb.net/My_homework_DB?retryWrites=true&w=majority&appName=hedgehog")

def generate_fake_contacts(num_contacts):
    fake = Faker()
    contacts = []
    for _ in range(num_contacts):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            preferred_contact_method=fake.random_element(elements=["email", "sms"]),
            message_sent=False
        )
        contact.save()
        contacts.append(contact)
    return contacts


def send_message_to_queue(contact_id):
    channel.basic_publish(
        exchange='',
        routing_key='email_queue',
        body=json.dumps({"contact_id": str(contact_id)}),
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )
    print(f" Надіслано повідомлення для контакту ID: {contact_id}")


def main():
    num_contacts = 10
    contacts = generate_fake_contacts(num_contacts)

    for contact in contacts:
        send_message_to_queue(contact.id)

    connection.close()


if __name__ == "__main__":
    main()