import tornado
from app.handlers import base

class ViewTermsAndConditionsHandler(base.BaseHandler):
    '''
    Renders the T&C page.    
    '''
    def on_get(self):
        self.base_render("landing/tc.html")