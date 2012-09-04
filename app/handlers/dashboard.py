import tornado
from app.handlers import base

class ViewDashBoardHandler(base.BaseHandler):
    '''
    Renders the dashboard page.    
    '''
    @tornado.web.authenticated
    def on_get(self):
        self.base_render("dashboard.html")
