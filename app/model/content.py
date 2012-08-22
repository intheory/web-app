from mongoengine import Document, StringField, ListField, IntField
# ============================ User ================================ #

class Question(Document):
    meta = {"collection":"Questions"}
    question = StringField(required=True)
    options = ListField(required=True, StringField, default=list)
    answer = IntField(required=True)
    
