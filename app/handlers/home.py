from app.handlers import base
from app.model.content import MiniQuizQuestion#!@UnresolvedImport

class HomePageHandler(base.BaseHandler):
    '''
    Renders the home page.    
    '''
    def on_get(self):
        questions = MiniQuizQuestion.objects                
        self.base_render("home.html", questions=questions)
        
class EvaluateHomeQuizHandler(base.BaseHandler):
    '''
    Evaluates homepage quiz
    '''
    def on_post(self):
        try:
            answers = self.get_argument("answers", None)
            answers    = answers.split(',')
            questions = MiniQuizQuestion.objects
            correct_answers = [question.answer for question in questions]
            count = 0
            for i in xrange(len(questions)):
                if set(int(answers[i])) == set(correct_answers[i]):
                    count += 1
            return (count,)
        except Exception, e:
            print e
    
    def on_success(self, score):
        self.xhr_response.update({"score": score}) 
        self.write(self.xhr_response)   