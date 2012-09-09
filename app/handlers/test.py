import tornado
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
        tid = self.get_argument("tid", None)
        answers = self.get_argument("answers", None)
        cursor = self.get_argument("cursor", None)
        print tid
        print answers
        print cursor          