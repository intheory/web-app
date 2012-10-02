
import tornado, tornado.escape
from app.handlers import base
from app.model.content import Section, Nugget, PractiseTest, MockTest, Test, Question, TestAnswer#!@UnresolvedImport
from random import shuffle
from mongoengine.queryset import DoesNotExist

TEST_SIZE = 5 

class CreateNewTestHandler(base.BaseHandler):
    '''
    Renders a test page. Note that if an argument is provided then that means that 
    this request came from a practise page. In this case we create a practise test.    
    '''
    @tornado.web.authenticated
    def on_get(self):

        #if an argument is passed then the test should be comprised of questions of a specific section
        sid = self.get_argument("sid", None)

        #Create new mock test object
        try:
            t = Test.objects(user=str(self.current_user.id), is_completed=False, cursor__ne=0).get()
            self.base_render("test/test.html", test=t, timed=True)
        except DoesNotExist, e:

            if sid:
                t = PractiseTest()
                timed = False
                questions = [question for question in Question.objects(sid=sid)] #Get questions related to that section
            else:
                t = MockTest()            
                questions = [question for question in Question.objects]
                timed = True

            t.user = str(self.current_user.id)
            shuffle(questions)
            t.questions = questions[:TEST_SIZE]
            t.score = 0

            #Initialize the answer list
            for q in t.questions:
                ta = TestAnswer()
                ta.qid = str(q.id)
                ta.selected_answers = []
                t.answers.append(ta)

            t.cursor = 0
            t.save()

            self.base_render("test/test.html", test=t, timed=timed)
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
            t = Test.objects(id=tid).get()
            test_type =  type(t)
            t.delete()
            #Create new mock test object
            t = test_type()
            t.user = str(self.current_user.id)
            questions = [question for question in Question.objects]
            shuffle(questions)
            t.questions = questions[:TEST_SIZE]
            t.score = 0

            #Initialize the answer list
            for q in t.questions:
                ta = TestAnswer()
                ta.qid = str(q.id)
                ta.selected_answers = [] 
                t.answers.append(ta)

            t.cursor = 0
            t.save()
            return (t,)
        except Exception, e:
            self.log.warning("Error while restarting a project:" + str(e))

    def on_success(self, t):
        self.xhr_response.update({"html": self.render_string("ui-modules/question.html", test=t, timed=True)})  
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
            t = Test.objects(id=tid).get()

            #Save user answers
            t.answers[int(cursor)].selected_answers = answers

            t.cursor += 1
            t.save()

            return (t,)
        except Exception, e:
            self.log.warning("Error while fetching new question " + str(e))

    def on_success(self, t):
        if t.cursor < len(t.questions): #is the test finished?
            self.xhr_response.update({"html": self.render_string("ui-modules/question.html", test=t)})  
        else:
            #Calculate test score 
            t.calculate_score()
            #Update user's points
            self.current_user.update_points(t.score)
            self.xhr_response.update({"html": self.render_string("ui-modules/complete.html", message="Test complete!", no_questions=len(t.questions), score=t.score, learn=False)})
        self.write(self.xhr_response) 

class GetPreviousQuestionHandler(base.BaseHandler):
    '''
    Fetches the previous question along with the selected answers.
    '''
    @tornado.web.authenticated
    def on_get(self):
        try:
            tid = self.get_argument("tid", None)
            t = Test.objects(id=tid).get()
            t.cursor -= 1
            t.save()
            return (t,)
        except Exception,e:
            print e
            
    def on_success(self, t):
        self.xhr_response.update({"html": self.render_string("ui-modules/question.html", test=t)})  
        self.write(self.xhr_response)

class DeleteTestHandler(base.BaseHandler):
    '''
    Deletes a test from the db. This happens when the user exits the browser
    before finishing a test.   
    '''
    @tornado.web.authenticated
    def on_post(self):
        tid = self.get_argument("tid", None)

        return
        
    def on_success(self):
        self.write(self.xhr_response)