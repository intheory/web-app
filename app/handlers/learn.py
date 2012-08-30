from app.handlers import base

class ViewProgressHandler(base.BaseHandler):
    '''
    Renders a page with the progress for each topic.    
    '''
    def on_get(self):
        self.base_render("learn.html")