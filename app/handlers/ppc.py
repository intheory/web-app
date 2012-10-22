from app.handlers import base, user
import tornado.web
from app.model.content import MockTest, MiniQuizQuestion#!@UnresolvedImport
from app.model.user import User
from app.model.content import HazardPerceptionClip, HazardPerceptionTest

class HP1Handler(base.BaseHandler):
    '''
    Renders the hp1 welcome page.    
    '''
    def on_get(self):
        version = self.get_argument("v", None)
        self.base_render("ppc/hp1.html", v=version)

class HP2Handler(base.BaseHandler):
    '''
    Renders the hp2 welcome page.    
    '''
    def on_get(self):
        version = self.get_argument("v", None)
        self.base_render("ppc/hp2.html", v=version)

class GetTwoClicksPaywallDashboardHandler(base.BaseHandler):
    '''
    Renders a 'fake' hazard perception dashboard which essentially redirects the users 
    to the payment page when they watch two videos.
    '''

    @tornado.web.authenticated
    def on_get(self):
        try:
            hpc = HazardPerceptionClip.objects
            hpt = HazardPerceptionTest.objects(uid=str(self.current_user.id))

            scores = {}
            for test in hpt:
                if str(test.id) not in scores: 
                    scores[str(test.id)] = test.score
                else:
                    if scores[str(test.id)] < test.score:
                        scores[str(test.id)] = test.score
                scores[str(test.cid)] = test.score
            
            self.base_render("ppc/learn-hazard-two-clicks.html", clips=hpc, has_seen=scores.keys(), older_scores=scores)
        except Exception, e:
            self.log.info("No hazard perception clips were found")
            self.base_render("ppc/learn-hazard-two-clicks.html", clips=None)


class GetClipPageHandler(base.BaseHandler):
    '''
    Gets the hazard perception clip page 
    '''
    @user.has_paid2 
    @tornado.web.authenticated
    def on_get(self):
        try:
            cid = self.get_argument("cid", None)
            hpc = HazardPerceptionClip.objects(id=cid).get()
            self.base_render("learn/learn-clip.html", cid=cid, path= hpc.base_dir + hpc.clip_name)
        except Exception, e:
            self.log.warning("Error while rendering clip page: " + str(e))

