from app.handlers import base

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
        rid = self.get_argument("rid", None)