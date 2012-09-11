from app.handlers import base
from app.model.content import MockTest, MiniQuizQuestion#!@UnresolvedImport
from app.model.user import User

class HomePageHandler(base.BaseHandler):
    '''
    Renders the home page.    
    '''
    def on_get(self):
        if  not self.current_user:
            questions = MiniQuizQuestion.objects                
            self.base_render("home.html", questions=questions, tweet="Woo hoo I passed my test. Thank you #intheory!")
        else:
            uid = self.current_user.id
            u = User.objects(id=uid).get()
            history = MockTest.objects(user=str(uid)) #TODO: create a model for user's history
            self.base_render("dashboard.html", user=u, history=history)

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
            
            #Put recorded user answers in buckets according to how many answers each
            #question has.
            user_answers = []
            for answer_list in correct_answers:
                l = []
                for i in  range(len(answer_list)):
                    l.append(int(answers.pop(0)))
                user_answers.append(l)

            for i in xrange(len(questions)):
                if set(user_answers[i]) == set(correct_answers[i]):
                    count += 1
            return (count,)
        except Exception, e:
            print e
    
    def on_success(self, score):
        self.xhr_response.update({"score": score}) 
        self.write(self.xhr_response)   