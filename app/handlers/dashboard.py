import tornado
from app.handlers import base
from app.model.user import User
from app.model.content import MockTest

class ViewDashBoardHandler(base.BaseHandler):
    '''
    Renders the dashboard page.    
    '''
    @tornado.web.authenticated
    def on_get(self):
    	uid = self.current_user.id
    	u = User.objects(id=uid).get()
    	history = MockTest.objects(user=str(uid)) #TODO: create a model for user's history
        self.base_render("dashboard.html", user=u, history=history)
