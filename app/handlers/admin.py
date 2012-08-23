from app.handlers import base
from app.model.content import Question#!@UnresolvedImport

class ViewAdminPanelHandler(base.BaseHandler):
    '''
    Renders admin panel
    '''
    def on_get(self):
        self.base_render("admin-main.html")

class ViewQuestionsHandler(base.BaseHandler):
    '''
    Displays a list of questions
    '''
    def on_get(self):
        self.base_render("admin-questions.html")

class AddQuestionHandler(base.BaseHandler):
    '''
    Adds a new question
    '''
    def on_post(self):
        try:
            question = self.get_argument("question-inp", None)
            option1 = self.get_argument("option1-inp", None)
            option2 = self.get_argument("option2-inp", None)
            option3 = self.get_argument("option3-inp", None)
            option4 = self.get_argument("option4-inp", None)
            q = Question()
            q.question = question
            q.options = [option1, option2, option3, option4]
            q.answer = 0
            q.save()
        except Exception, e:
            print e
        