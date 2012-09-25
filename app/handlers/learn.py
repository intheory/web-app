import tornado, tornado.escape, math
from app.handlers import base
from app.model.content import Section, Nugget, MiniQuizQuestion, HazardPerceptionClip, HazardPerceptionTest#!@UnresolvedImport
from mongoengine.queryset import DoesNotExist

class ViewLearnMainHandler(base.BaseHandler):
    '''
    Renders a page with the progress for each topic.    
    '''
    @tornado.web.authenticated
    def on_get(self):
        sections = Section.objects
        self.base_render("learn/learn-main.html", sections= sections)

class ViewSectionHandler(base.BaseHandler):
    '''
    Renders a section page.    
    '''
    @tornado.web.authenticated
    def on_get(self):
        try:
            sid = self.get_argument("sid")
            #Get section object
            section = Section.objects(id=sid).get()

            #Get either the first nugget of the section or where the user left it off.
            nugget = section.nuggets[0]
            self.base_render("learn/learn-content.html", section=section, 
                                                         nugget=nugget, 
                                                         cursor=0, 
                                                         section_length=len(section.nuggets))
        except Exception, e:
            self.log.warning(str(e))    

class GetPreviousNuggetHandler(base.BaseHandler):
    '''
    Gets the previous nugget
    '''
    def on_get(self):
        sid = self.get_argument("sid", None)
        cursor = self.get_argument("cursor", None)
        section = Section.objects(id=sid).get()
        new_cursor = int(cursor)-1
        previous_nugget = section.nuggets[new_cursor]
        return (section, previous_nugget, new_cursor, len(section.nuggets))

    def on_success(self,section, n, new_cursor, section_length):
        if self.is_xhr:
            html = self.render_string("ui-modules/nugget.html", section=section,
                                                        nugget=n,
                                                        cursor=new_cursor,
                                                        section_length=section_length)
            self.xhr_response.update({"html":html})
            self.write(self.xhr_response)

class GetNextNuggetHandler(base.BaseHandler):
    '''
    Gets the next nugget
    '''
    def on_get(self):
        try:
            sid = self.get_argument("sid", None)
            cursor = self.get_argument("cursor", None)
            section = Section.objects(id=sid).get()
            new_cursor = int(cursor)+1
            if new_cursor == len(section.nuggets): #if we reached the end of the section
                new_cursor = int(cursor)
                next_nugget = None
                new_cursor += 1
            else:
                next_nugget = section.nuggets[new_cursor]
        except Exception, e:
            self.log.warning(str(e))
        return (section, next_nugget, new_cursor, len(section.nuggets))

    def on_success(self, section, n, new_cursor, section_length):
        if self.is_xhr:
            if n: #if there exists a next nugget (not end of section)
                html = self.render_string("ui-modules/nugget.html", section=section,
                                                            nugget=n,
                                                            cursor=new_cursor,
                                                            section_length=section_length)
                self.xhr_response.update({"html":html})
            else:
                self.xhr_response.update({"html": self.render_string("ui-modules/complete.html", message="Section Completed!", no_questions=0, score=0, learn=True)})
            self.write(self.xhr_response)

class GetQuestionHandler(base.BaseHandler):
    '''
    Gets a new question
    '''
    @tornado.web.authenticated
    def on_get(self):
        sid = self.get_argument("sid", None)
        question = MiniQuizQuestion.objects[0]
        html = self.render_string("ui-modules/question.html", question = question)
        return (html,)

    def on_success(self, html):
        if self.is_xhr:
            self.xhr_response.update({"html": html})
            self.write(self.xhr_response) 

class GetHazardPerceptionHandler(base.BaseHandler):
    '''
    Gets the hazard perception clips 
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
            
            self.base_render("learn/learn-hazard.html", clips=hpc, has_seen=scores.keys(), older_scores=scores)
        except Exception, e:
            self.log.info("No hazard perception clips were found")
            self.base_render("learn/learn-hazard.html", clips=None)

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
            for a in answers:
                for ca in correct_answers:
                    if math.fabs(a-ca) < 2:
                        score+=1
                        correct_answers.remove(ca)

            return (cid, score, clip.solution_clip_name, len(answers))
        except Exception, e:
            self.log.warning(str(e))

    def on_success(self, cid, score, solution_clip_name, clicks): 
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
            html = self.render_string("ui-modules/complete-video.html", clip=solution_clip_name, score=score, accuracy=score/clicks)
            self.xhr_response.update({"html": html})
            self.write(self.xhr_response) 