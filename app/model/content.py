from mongoengine import Document, DictField, EmbeddedDocument, FloatField, EmbeddedDocumentField, StringField, ListField, IntField, BooleanField, ReferenceField, DateTimeField
from datetime import datetime
# ============================ User ================================ #

class Question(Document):
    meta = {"collection":"Questions"}
    question = StringField(required=True)
    options = ListField(StringField(), default=list, required=True)
    answer = ListField(StringField(), required=True)
    sid = StringField(required=True, default="")
    extract = StringField(required=True, default="")
    image = StringField(required=False)
    question_number = StringField(required=True)
    
class MiniQuizQuestion(Document):
    meta = {"collection":"MiniQuizQuestions"}
    question = StringField(required=True)
    options = ListField(StringField(), default=list, required=True)
    answer = ListField(IntField(), required=True)
    
class Nugget(EmbeddedDocument):
    section_sub_title = StringField(required=True)
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

class Test(Document):
    meta = {"collection":"Tests", 'allow_inheritance': True}
    user = StringField(required=True)
    questions = ListField(ReferenceField(Question), required=True, default=list)
    answers = ListField(EmbeddedDocumentField(TestAnswer), default=list)
    score = IntField(required=True, default=0)
    cursor = IntField(required=True, default=0) #Indicates which question is currently viewed
    is_completed = BooleanField(required=True, default=False)

    def calculate_score(self):
        '''
        Calculates the test score based on user's answers
        '''
        #Put all correct answers in a list
        correct_answers = []
        for question in self.questions:
            correct_answers.append([int(answer) for answer in question.answer])                

        #Put all user's answers in a list
        user_answers = []
        for user_answer in self.answers:
            user_answers.append([int(answer) for answer in user_answer.selected_answers])

        #Check if user answered correctly by looking at the intersection of correct answers and user answers
        for i, correct_answer in enumerate(correct_answers):                
            user_answer = user_answers[i]
            inter = set(user_answer).intersection(correct_answer)
            if len(inter) == len(correct_answer): 
                self.score += 1
        self.is_completed = True
        self.save()

    def update_cursor(self, value):
        self.cursor += value
        self.save()

class MockTest(Test):
    pass
    #In the future this test will have some different features than the Practise test

class PractiseTest(Test):
    
    def evaluate_question(self, cursor, user_answer):
        '''
        Evaluates the question at cursor position
        '''
        try:
            #Put correct answers in a list
            correct_answers =[int(answer) for answer in self.questions[cursor].answer]

            #Put user's answers in a list
            user_answers = [int(answer) for answer in user_answer.selected_answers]

            #Check if user answered correctly by looking at the intersection of correct answers and user answers
            inter = set(user_answers).intersection(correct_answers)
            if len(inter) == len(correct_answers): 
                return 1
            else:
                return 0
        except Exception, e:
            print e


class HazardPoint(EmbeddedDocument):
    start = IntField(required=True) #When the hazard occurs initially
    end = IntField(required=True)

class HazardPerceptionClip(Document):
    meta = {"collection":"HazardPerceptionClips"}
    base_dir = StringField(required=True)
    clip_name = StringField(required=True)
    hazards = ListField(EmbeddedDocumentField(HazardPoint), required=True)
    solution_clip_name = StringField(required=True)

class HazardPerceptionTest(Document):
    meta = {"collection":"HazardPerceptionTests"}
    uid = StringField(required=True)
    cid = StringField(required=True)
    score = IntField(required=True, default=0)

class FeedbackItem(Document):
    meta = {"collection":"FeedbackItems"}
    description = StringField(required=True)
    uid = StringField(required=True)
    timestamp = DateTimeField(required=True, default=datetime.now())