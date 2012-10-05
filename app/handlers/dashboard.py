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
        print self.request
    	uid = self.current_user.id
    	u = User.objects(id=uid).get()
        stats = u.get_user_stats()
        progress = u.get_overall_progress()
        self.base_render("dashboard.html", user=u, 
                                           progress = progress,
        								   correct_answers=stats['correct_answers'], 
        								   points=stats['points'],
        								   accuracy="{0:.1f}".format(stats['accuracy']))
