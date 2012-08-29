from app.handlers import base

class ViewDashBoardHandler(base.BaseHandler):
    '''
    Renders the dashboard page.    
    '''
    def on_get(self):
        self.base_render("dashboard.html")
