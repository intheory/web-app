from mongoengine import Document, StringField, ListField, IntField
# ============================ User ================================ #

class Question(Document):
    meta = {"collection":"Questions"}
    question = StringField(required=True)
    options = ListField(StringField(), default=list, required=True)
    answer = ListField(StringField(), required=True)
    
class MiniQuizQuestion(Document):
    meta = {"collection":"MiniQuizQuestions"}
    question = StringField(required=True)
    options = ListField(StringField(), default=list, required=True)
    answer = ListField(IntField(), required=True)
    
class Section(Document):
    meta = {"collection":"Sections"}
    title = StringField(required=True)

class Nugget(Document):
    meta = {"collection":"Nuggets"}
    title = StringField(required=True)
    img = StringField(required=True)
    content = StringField(required=True)
    section = StringField(required=True)
    next_nugget = StringField(required=True)
    previous_nugget = StringField(required=True)    