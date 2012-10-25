import tornado, tornado.escape
from app.handlers import base, user
from app.model.content import Section, Nugget, PractiseTest, MockTest, Test, Question, TestAnswer#!@UnresolvedImport
from random import shuffle
from mongoengine.queryset import DoesNotExist

MOCK_TEST_SIZE = 50
PRACTISE_TEST_SIZE = 20 


class CreateNewTestHandler(base.BaseHandler):
    '''
    Renders a test page. Note that if an argument is provided then that means that 
    this request came from a practise page. In this case we create a practise test.    
    '''
    @user.has_paid 
    def on_get(self):

        #if an argument is passed then the test should be comprised of questions of a specific section
        sid = self.get_argument("sid", None)

        #Create new mock test object
        try:
            if sid:
                try:
                    t = PractiseTest.objects(user=str(self.current_user.id), is_completed=False, cursor__ne=0).get()
                    self.base_render("test/test.html", test=t, timed=False, existing=True)
                    return
                except DoesNotExist, e:
                    t = PractiseTest()
                    timed = False
                    questions = [question for question in Question.objects(sid=sid)] #Get questions related to that section
                    shuffle(questions)
                    questions = questions[:PRACTISE_TEST_SIZE]
            else:
                t = MockTest()            
                questions = [question for question in Question.objects]
                shuffle(questions)
                questions = questions[:MOCK_TEST_SIZE]

                timed = True

            t.user = str(self.current_user.id)
            t.questions = questions
            t.score = 0

            t.cursor = 0
            t.save()

            self.base_render("test/test.html", test=t, timed=timed)
        except Exception, e:
            self.log.warning("Error while creating a new " + str(type(t)) + " : " + str(e))

class GetNewTestHandler(base.BaseHandler):
    '''
    Renders a new test page after the user decided to dismiss their last unfinished test.  
    This is only applicable for practise tests. Mock tests are deleted if left unfinished.  
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
            t.questions = questions[:PRACTISE_TEST_SIZE]
            t.score = 0
            t.cursor = 0
            t.save()
            return (t,)
        except Exception, e:
            self.log.warning("Error while restarting a test: " + str(e))

    def on_success(self, t):
        if isinstance(t, MockTest):
            timed = True
        elif isinstance(t, PractiseTest):
            timed = False
        self.xhr_response.update({"html": self.render_string("ui-modules/question.html", test=t, timed=timed)})  
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
            timer_is_over = self.get_argument("timer_over", None)

            #Fetch the test object
            t = Test.objects(id=tid).get()
            #Save user answers  
            t.save_answers(answers)

            #if this request is made because the timer is over evaluate the test and 
            #end it
            if timer_is_over:
                t.cursor = 50
                t.save()
                return (t, True)

            #This will only be executed for practice tests
            if isinstance(t, PractiseTest):
                result = t.evaluate_question(int(cursor))
                if result == 1:
                    correct = True
                    t.update_cursor(1)
                elif result == 0:
                    correct = False;
            else:
                #if this is a mock test jsut increase cursor and 
                #assume it's correct
                t.update_cursor(1)
                correct = True

            return (t, correct)
        except Exception, e:
            self.log.warning("Error while fetching new question: " + str(e))

    def on_success(self, t, correct):
        if isinstance(t, MockTest):
            timed = True
        elif isinstance(t, PractiseTest):
            timed = False

        if t.cursor < len(t.questions): #is the test finished?
            if correct:
                self.xhr_response.update({"correct": correct, "html": self.render_string("ui-modules/question.html", test=t, timed=timed)}) 
            else:
                self.xhr_response.update({"correct": correct,
                                          "html": self.render_string("ui-modules/explanation.html", test=t, question=t.questions[t.cursor])})
        else:
            if correct:
                #Calculate test score 
                t.calculate_score()
                #Update user's points
                self.current_user.update_points(t.score)
                self.xhr_response.update({"html": self.render_string("ui-modules/complete.html", message="Test complete!", no_questions=len(t.questions), score=t.score, learn=False)})
            else:
                self.xhr_response.update({"correct": correct, "html": self.render_string("ui-modules/question.html", test=t, timed=timed)}) 
        self.write(self.xhr_response) 

class GetNextAfterWrongQuestionHandler(base.BaseHandler):
    '''
    Simply fetches the next question after a wrong answer dialog.
    '''
    @tornado.web.authenticated
    def on_get(self):
        try:
            tid = self.get_argument("tid", None) 

            #Fetch the test object
            t = Test.objects(id=tid).get()
            t.update_cursor(1)    
            return (t,)
        except Exception, e:
            self.log.warning("Error while fetching new question after wrong answer dialog: " + str(e))

    def on_success(self, t):
        if isinstance(t, MockTest):
            timed = True
        elif isinstance(t, PractiseTest):
            timed = False

        if t.cursor < len(t.questions): #is the test finished?
            self.xhr_response.update({"html": self.render_string("ui-modules/question.html", test=t, timed=timed)})
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
        if isinstance(t, MockTest):
            timed = True
        elif isinstance(t, PractiseTest):
            timed = False
        self.xhr_response.update({"html": self.render_string("ui-modules/question.html", test=t, timed=timed)})  
        self.write(self.xhr_response)

class DeleteTestHandler(base.BaseHandler):
    '''
    Deletes a test from the db. This happens when the user exits the browser
    before finishing a test.   
    '''
    @tornado.web.authenticated
    def on_post(self):  
        tid = self.get_argument("tid", None)
        t = Test.objects(id=tid).get()
        if len(t.answers) == 0 or isinstance(t, MockTest): #if the user didn't start doing the test and left the page then delete the test.            
            t.delete()
        return
        
    def on_success(self):
        self.write(self.xhr_response)