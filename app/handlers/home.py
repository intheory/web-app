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
            self.base_render("home.html")
        else:
            uid = self.current_user.id
            u = User.objects(id=uid).get()
            history = MockTest.objects(user=str(uid)) #TODO: create a model for user's history
            self.redirect("/dashboard")


class LoginScreenHandler(base.BaseHandler):
    '''
    Renders the login page.    
    '''
    def on_get(self):
        next = self.get_argument("next", None)
        if not next:
            next = "/dashboard"
        self.base_render("login.html", next=next)