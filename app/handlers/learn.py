import tornado
from app.handlers import base
from app.model.content import Section, Nugget, MiniQuizQuestion#!@UnresolvedImport

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
        return (previous_nugget, new_cursor, len(section.nuggets))

    def on_success(self, n, new_cursor, section_length):
        if self.is_xhr:
            nugget = {"nugget_title": n.title,
                      "nugget_img": n.img,
                      "nugget_content": n.content,
                      "new_cursor": new_cursor,
                      "section_length": section_length
                      }
            self.xhr_response.update(nugget)
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
        return (next_nugget, new_cursor, len(section.nuggets))

    def on_success(self, n, new_cursor, section_length):
        if self.is_xhr:
            if n: #if there exists a next nugget (not end of section)
                nugget = {"nugget_title": n.title,
                          "nugget_img": n.img,
                          "nugget_content": n.content,
                          "new_cursor": new_cursor,
                          "section_length": section_length    
                          }
                self.xhr_response.update(nugget)
            else:
                self.xhr_response.update({"html": self.render_string("ui-modules/complete.html", message="Section Completed!", no_questions=10, score=2, learn=True)})
            self.write(self.xhr_response)

class GetQuestionHandler(base.BaseHandler):
    '''
    Gets a new question
    '''
    def on_get(self):
        sid = self.get_argument("sid", None)
        question = MiniQuizQuestion.objects[0]
        html = self.render_string("ui-modules/question.html", question = question)
        return (html,)

    def on_success(self, html):
        if self.is_xhr:
            self.xhr_response.update({"html": html})
            self.write(self.xhr_response)    
