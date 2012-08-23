from app.handlers import base
from app.model.content import Question#!@UnresolvedImport

class HomePageHandler(base.BaseHandler):
    '''
    Renders the home page.    
    '''
    def on_get(self):
        questions = Question.objects
        self.base_render("home.html", questions=questions)