import tornado, tornado.escape
from app.handlers import base
from app.model.content import Section

class ViewPracticeMainHandler(base.BaseHandler):
    '''
    Renders the main practise page.    
    '''
    def on_get(self):
        sections = Section.objects
        self.base_render("practice/practice-main.html", sections=sections)