from app.handlers import base

class HomePageHandler(base.BaseHandler):
    '''
    Renders the home page.    
    '''
    def on_get(self):
        
        self.base_render("home.html")