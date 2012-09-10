import tornado, tornado.escape
from app.handlers import base
from app.model.content import Section, Nugget, MockTest, MiniQuizQuestion#!@UnresolvedImport

class GetNewTestHandler(base.BaseHandler):
    '''
    Renders a test page.    
    '''
    @tornado.web.authenticated
    def on_get(self):
        #Create new mock test object
        try:
            mt = MockTest()
            mt.user = str(self.current_user.id)
            mt.questions = [question for question in MiniQuizQuestion.objects]
            mt.score = 0
            mt.cursor = 0
            mt.save()
            self.base_render("test/test.html", test=mt)
        except Exception, e:
            print e

class EvaluateTestQuestionHandler(base.BaseHandler):
    '''
    Evaluates a given question and updates score for the test.    
    '''
    @tornado.web.authenticated
    def on_post(self): 
        try:
            tid = self.get_argument("tid", None)
            answers = self.get_argument("answers", None)
            if answers:
                answers = tornado.escape.json_decode(answers)
            cursor = self.get_argument("cursor", None)
            
            #Fetch the test object
            mt = MockTest.objects(id=tid).get()
            
            #Fetch the question in hand and the correct answers
            cursor = int(cursor)
            q = mt.questions[cursor]
            correct_answers = q.answer
            #Check if user answered correctly.
            inter = set(answers).intersection(correct_answers)
            if len(inter) == len(correct_answers): 
                mt.score += 1
            mt.cursor += 1
            mt.save()
            return (mt,)
        except Exception, e:
            print e

    def on_success(self, mt):
        if mt.cursor < len(mt.questions):
            self.xhr_response.update({"html": self.render_string("ui-modules/question.html", test=mt)})  
        else:
            #self.xhr_response.update({"html": "<p>Your score is "+str(mt.score)+"</p>"})
            self.xhr_response.update({"html": self.render_string("ui-modules/complete.html", message="Congratulations!", no_questions=len(mt.questions), score=mt.score, learn=False)})
        self.write(self.xhr_response) 