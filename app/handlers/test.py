
import tornado, tornado.escape
from app.handlers import base
from app.model.content import Section, Nugget, MockTest, Question, TestAnswer#!@UnresolvedImport
from random import shuffle
from mongoengine.queryset import DoesNotExist

TEST_SIZE = 5 

class CreateNewTestHandler(base.BaseHandler):
    '''
    Renders a test page.    
    '''
    @tornado.web.authenticated
    def on_get(self):
        #Create new mock test object
        try:
            mt = MockTest.objects(user=str(self.current_user.id), is_completed=False).get()
            self.base_render("test/test.html", test=mt, timed=True)
        except DoesNotExist, e:
            mt = MockTest()
            mt.user = str(self.current_user.id)
            questions = [question for question in Question.objects]
            shuffle(questions)
            mt.questions = questions[:TEST_SIZE]
            mt.score = 0

            #Initialize the answer list
            for q in mt.questions:
                ta = TestAnswer()
                ta.qid = str(q.id)
                ta.selected_answers = [] 
                mt.answers.append(ta)

            mt.cursor = 0
            mt.save()
            self.base_render("test/test.html", test=mt, timed=True)
        except Exception, e:
            self.log.warning(str(e))

class GetNewTestHandler(base.BaseHandler):
    '''
    Renders a new test page after the user decided to dismiss their last unfinished test.    
    '''
    def on_get(self):
        try:
            #Delete the old test
            tid = self.get_argument("tid", None)
            t = MockTest.objects(id=tid).get()
            t.delete()
            #Create new mock test object
            mt = MockTest()
            mt.user = str(self.current_user.id)
            questions = [question for question in Question.objects]
            shuffle(questions)
            mt.questions = questions[:TEST_SIZE]
            mt.score = 0

            #Initialize the answer list
            for q in mt.questions:
                ta = TestAnswer()
                ta.qid = str(q.id)
                ta.selected_answers = [] 
                mt.answers.append(ta)

            mt.cursor = 0
            mt.save()
            return (mt,)
        except Exception, e:
            self.log.warning(str(e))

    def on_success(self, mt):
        self.xhr_response.update({"html": self.render_string("ui-modules/question.html", test=mt)})  
        self.write(self.xhr_response) 

class GetNextQuestionHandler(base.BaseHandler):
    '''
    Fetches next question.    
    '''
    @tornado.web.authenticated
    def on_get(self): 
        try:
            tid = self.get_argument("tid", None)
            answers = self.get_argument("answers", None)
            if answers:
                answers = tornado.escape.json_decode(answers)
            cursor = self.get_argument("cursor", None)

            #Fetch the test object
            mt = MockTest.objects(id=tid).get()

            #Save user answers
            mt.answers[int(cursor)].selected_answers = answers

            mt.cursor += 1
            mt.save()

            return (mt,)
        except Exception, e:
            self.log.warning("Error while fetching new question" + str(e))

    def on_success(self, mt):
        if mt.cursor < len(mt.questions): #is the test finished?
            self.xhr_response.update({"html": self.render_string("ui-modules/question.html", test=mt)})  
        else:
            #Calculate test score 
            mt.calculate_score()
            #Update user's points
            self.current_user.update_points(mt.score)
            self.xhr_response.update({"html": self.render_string("ui-modules/complete.html", message="Test complete!", no_questions=len(mt.questions), score=mt.score, learn=False)})
        self.write(self.xhr_response) 

class GetPreviousQuestionHandler(base.BaseHandler):
    '''
    Fetches the previous question along with the selected answers.
    '''
    @tornado.web.authenticated
    def on_get(self):
        try:
            tid = self.get_argument("tid", None)
            mt = MockTest.objects(id=tid).get()
            mt.cursor -= 1
            mt.save()
            return (mt,)
        except Exception,e:
            print e
            
    def on_success(self, mt):
        self.xhr_response.update({"html": self.render_string("ui-modules/question.html", test=mt)})  
        self.write(self.xhr_response)

class DeleteTestHandler(base.BaseHandler):
    '''
    Deletes a test from the db. This happens when the user exits the browser
    before finishing a test.   
    '''
    @tornado.web.authenticated
    def on_post(self):
        tid = self.get_argument("tid", None)
        print tid
        return
        
    def on_success(self):
        self.write(self.xhr_response)