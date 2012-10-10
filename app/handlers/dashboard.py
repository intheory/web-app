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
        progress = u.get_overall_progress()
        self.base_render("dashboard.html", user=u, 
                                           progress = progress,
                                           stats= stats)

class RemoveDashBoardMsgHandler(base.BaseHandler):
    '''
    Removes the dashboard welcome messgae.    
    '''
    @tornado.web.authenticated
    def on_post(self):
        self.current_user.mark_welcome_msg_as_read()
        self.write(self.xhr_response) 