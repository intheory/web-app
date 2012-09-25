from mongoengine import Document, StringField, DateTimeField

class Log(Document):
    meta = {"collection":"Log"}
    name = StringField(required=True)
    filename = StringField(required=True)
    timestamp = DateTimeField(required=True)
    level = StringField(required=True)
    message = StringField(required=True)