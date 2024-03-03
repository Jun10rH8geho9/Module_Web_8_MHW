from mongoengine import Document, StringField, ReferenceField, ListField, BooleanField, CASCADE

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=30)
    born_location = StringField(max_length=200)
    description = StringField()
    meta = {"collection": "authors"}

class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()
    tags = ListField(StringField(max_length=15))
    meta = {"collection": "quotes"}

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    phone_number = StringField(required=True)
    message_sent = BooleanField(default=False)
    preferred_contact_method = StringField(choices=["email", "sms"])
    meta = {"collection": "contacts"}