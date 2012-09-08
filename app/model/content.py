from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, StringField, ListField, IntField, BooleanField
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
    
class Nugget(EmbeddedDocument):
    title = StringField(required=True)
    img = StringField(required=True)
    content = StringField(required=True)

class Section(Document):
    meta = {"collection":"Sections"}
    title = StringField(required=True)
    nuggets = ListField(EmbeddedDocumentField(Nugget), default=list)

class MockTest(Document):
    meta = {"collection":"MockTests"}
    user = StringField(required=True)
    questions = ListField(Question(), required=True, default=list)
    score = IntField(required=True, default=0)
    cursor = IntField(required=True, default=0) #Indicates which question is currently viewed