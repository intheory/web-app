from mongoengine import Document, DictField, EmbeddedDocument, FloatField, EmbeddedDocumentField, StringField, ListField, IntField, BooleanField, ReferenceField
# ============================ User ================================ #

class Question(Document):
    meta = {"collection":"Questions"}
    question = StringField(required=True)
    options = ListField(StringField(), default=list, required=True)
    answer = ListField(StringField(), required=True)
    sid = StringField(required=True, default="")
    extract = StringField(required=True, default="")
    image = StringField(required=False)
    
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
    questions = ListField(ReferenceField(Question), required=False, default=list)

class TestAnswer(EmbeddedDocument):
    qid = StringField(required=True, default="")
    selected_answers = ListField(IntField(), required=True, default=list)

class MockTest(Document):
    meta = {"collection":"MockTests"}
    user = StringField(required=True)
    questions = ListField(ReferenceField(Question), required=True, default=list)
    answers = ListField(EmbeddedDocumentField(TestAnswer), default=list)
    score = IntField(required=True, default=0)
    cursor = IntField(required=True, default=0) #Indicates which question is currently viewed

class HazardPerceptionClip(Document):
    meta = {"collection":"HazardPerceptionClips"}
    base_dir = StringField(required=True)
    clip_name = StringField(required=True)
    hazards = ListField(FloatField(), required=True)
    solution_clip_name = StringField(required=True)

class HazardPerceptionTest(Document):
    meta = {"collection":"HazardPerceptionTests"}
    uid = StringField(required=True)
    cid = StringField(required=True)
    score = IntField(required=True, default=0)