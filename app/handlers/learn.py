import tornado, tornado.escape, math
from app.handlers import base
from app.model.content import Section, Nugget, MiniQuizQuestion, HazardPerceptionClip#!@UnresolvedImport
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
            print e    

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
            print e
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
    def on_get(self):
        try:
            hpc = HazardPerceptionClip.objects
            self.base_render("learn/learn-hazard.html", clip=hpc[0])
        except Exception, e:
            self.base_render("learn/learn-hazard.html", clip=None)

class EvaluateHazardPerceptionHandler(base.BaseHandler):
    '''
    Evaluates a user's answers for a hazard perception clip
    '''
    def on_post(self):
        try:
            cid = self.get_argument("cid", None)
            answers = self.get_argument("answers", None)
            if answers:
                answers = tornado.escape.json_decode(answers)
            answers = [float(answer) for answer in answers]
            correct_answers = HazardPerceptionClip.objects(id=cid).get().hazards
            score = 0
            for a in answers:
                for ca in correct_answers:
                    if math.fabs(a-ca) < 2:
                        score+=1

            return (score,)
        except Exception, e:
            print e

    def on_success(self, score): 
        if self.is_xhr:
            self.xhr_response.update({"score": score})
            self.write(self.xhr_response) 