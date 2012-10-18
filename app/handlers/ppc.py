from app.handlers import base
from app.model.content import MockTest, MiniQuizQuestion#!@UnresolvedImport
from app.model.user import User

class HP1Handler(base.BaseHandler):
    '''
    Renders the hp1 welcome page.    
    '''
    def on_get(self):
        version = self.get_argument("v", None)
        self.base_render("ppc/hp1.html", v=version)