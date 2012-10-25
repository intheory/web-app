import math
from app.handlers import base, user
import tornado.web
from app.model.content import MockTest, MiniQuizQuestion#!@UnresolvedImport
from app.model.user import User
from app.model.content import HazardPerceptionClip, HazardPerceptionTest

########################## Hazard Perception PPC ##########################
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
    def on_get(self):
        try:
            hpc = HazardPerceptionClip.objects
            if self.current_user:
                hpt = HazardPerceptionTest.objects(uid=str(self.current_user.id))

                scores = {}
                for test in hpt:
                    if str(test.id) not in scores: 
                        scores[str(test.id)] = test.score
                    else:
                        if scores[str(test.id)] < test.score:
                            scores[str(test.id)] = test.score
                    scores[str(test.cid)] = test.score
            else:
                scores={}
            
            self.base_render("ppc/learn-hazard-two-clicks.html", clips=hpc, has_seen=scores.keys(), older_scores=scores)
        except Exception, e:
            print e
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

class GetIntroClipPageHandler(base.BaseHandler):
    '''
    Gets the hazard perception introduction clip page 
    '''
    @tornado.web.authenticated
    def on_get(self):
        try:
            self.base_render("learn/learn-clip.html", cid="intro", path= "/obj/video/intro")
        except Exception, e:
            self.log.warning("Error while rendering clip page: " + str(e))

class EvaluateHazardPerceptionHandler(base.BaseHandler):
    '''
    Evaluates a user's answers for a hazard perception clip
    '''
    @tornado.web.authenticated
    def on_post(self):
        try:
            cid = self.get_argument("cid", None)
            answers = self.get_argument("answers", None)
            if answers:
                answers = tornado.escape.json_decode(answers)
            answers = [float(answer) for answer in answers]
            clip = HazardPerceptionClip.objects(id=cid).get()
            correct_answers = clip.hazards
            score = 0
            hits = 0
            for a in answers:
                for ca in correct_answers:
                    lower_limit = ca.start
                    upper_limit = ca.end
                    if lower_limit <= a <= upper_limit :
                        hits += 1
                        #Simple linear interpolation to get the score. The sooner u spot the hazard the more the points
                        points = 5 * (1 - (a - lower_limit) / (upper_limit-lower_limit))
                        score+= int(math.ceil(points))
                        correct_answers.remove(ca)

            return (cid, score, clip.solution_clip_name, len(answers), hits)
        except Exception, e:
            self.log.warning(str(e))

    def on_success(self, cid, score, solution_clip_name, clicks, hits): 
        #Create a new test and save the score
        hpt = HazardPerceptionTest()
        hpt.uid = str(self.current_user.id)
        hpt.cid = cid
        hpt.score = score
        hpt.save()

        #Update user's points
        self.current_user.update_points(score)

        if self.is_xhr:
            if clicks==0: clicks+=1 # Avoid ZeroDivisionError
            html = self.render_string("ppc/complete-video-ppc.html", clip=solution_clip_name, score=score, accuracy=float(hits)/clicks)
            self.xhr_response.update({"html": html})
            self.write(self.xhr_response) 

########################## Practice Tests PPC ##########################
class PT1Handler(base.BaseHandler):
    '''
    Renders the PT welcome page.    
    '''
    def on_get(self):
        version = self.get_argument("v", None)
        self.base_render("ppc/pt1.html", v=version)

