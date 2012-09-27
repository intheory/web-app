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
    	stats = u.get_user_stats()
        self.base_render("dashboard.html", user=u, 
        								   correct_answers=stats['correct_answers'], 
        								   points=stats['points'],
        								   accuracy="{0:.1f}".format(stats['accuracy']))
