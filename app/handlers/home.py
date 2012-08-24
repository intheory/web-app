from app.handlers import base
from app.model.content import Question#!@UnresolvedImport

class HomePageHandler(base.BaseHandler):
    '''
    Renders the home page.    
    '''
    def on_get(self):
        questions = Question.objects
        self.base_render("home.html", questions=questions)
        
class EvaluateHomeQuizHandler(base.BaseHandler):
    '''
    Evaluates homepage quiz
    '''
    def on_post(self):
        answers = self.get_argument("answers", None)
        answers    = answers.split(',')
        questions = Question.objects
        correct_answers = [question.answer for question in questions]
        count = 0
        for i in xrange(len(questions)):
            if int(answers[i]) == correct_answers[i]:
                count += 1
        return (count,)
    
    def on_success(self, score):
        self.xhr_response.update({"score": score}) 
        self.write(self.xhr_response)   