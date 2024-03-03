import json
from bson import ObjectId
from models import Author, Quote
from mongoengine import connect


def load_data():
    connect(db='My_homework_DB', host="mongodb+srv://web_8MHW:oulGmMDL5ksPq6fz@hedgehog.rsn29se.mongodb.net/My_homework_DB?retryWrites=true&w=majority&appName=hedgehog")

    # Завантажуємо дані авторів
    with open('authors.json', encoding='utf-8') as f:
        authors_data = json.load(f)

    # Зберігаємо дані авторів у базу даних
    for author in authors_data:
        author_doc = Author.objects(fullname=author['fullname']).first()
        if not author_doc:
            author_doc = Author(**author)
            author_doc.save()

    # Завантажуємо дані цитат з файлу quotes.json
    with open('qoutes.json', encoding='utf-8') as f:
        quotes_data = json.load(f)

    # Збереження цитат у базу даних
    for quote in quotes_data:
        author = Author.objects(fullname=quote['author']).first()
        if author:
            quote_doc = Quote(author=ObjectId(author.id), quote=quote['quote'], tags=quote['tags'])
            quote_doc.save()

if __name__ == "__main__":
    load_data()