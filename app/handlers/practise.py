
import tornado, tornado.escape
from app.handlers import base
from app.model.content import Section


class ViewPractiseMainHandler(base.BaseHandler):
    '''
    Renders the main practise page.    
    '''
    @tornado.web.authenticated
    def on_get(self):
        sections = Section.objects
        self.base_render("practise/practise-main.html", sections=sections)