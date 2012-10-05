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
    selected_answers = ListField(IntField(), default=list)

class MockTest(Document):
    meta = {"collection":"MockTests"}
    user = StringField(required=True)
    questions = ListField(ReferenceField(Question), required=True, default=list)
    answers = ListField(EmbeddedDocumentField(TestAnswer), required=True, default=list)
    score = IntField(required=True, default=0)
    cursor = IntField(required=True, default=0) #Indicates which question is currently viewed

    def calculate_score(self):
        '''
        Calculates the test score based on user's answers
        '''
        correct_answers = []
        #Fetch the question in hand and the correct answers
        for question in self.questions:
            correct_answers.append([int(answer) for answer in question.answer])                

        user_answers = []
        for user_answer in self.answers:
            user_answers.append([int(answer) for answer in user_answer.selected_answers])

        for i, correct_answer in enumerate(correct_answers):                
            #Check if user answered correctly.
            user_answer = user_answers[i]
            inter = set(user_answer).intersection(correct_answer)
            if len(inter) == len(correct_answer): 
                self.score += 1
        self.save()

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