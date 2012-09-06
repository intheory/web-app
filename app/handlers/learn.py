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

class ViewQuestionHandler(base.BaseHandler):
    '''
    Gets a new question for viewing.
    '''
    @tornado.web.authenticated
    def on_get(self):
        question = MiniQuizQuestion.objects[0]
        return (question,)
    
    def on_success(self, q):
        self.base_render("learn/learn-question.html", question=q)

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
        return (previous_nugget, new_cursor)

    def on_success(self, n, new_cursor):
        if self.is_xhr:
            nugget = {"nugget_title": n.title,
                      "nugget_img": n.img,
                      "nugget_content": n.content,
                      "new_cursor": new_cursor
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
            next_nugget = section.nuggets[new_cursor]
        except Exception, e:
            print e
        return (next_nugget, new_cursor)

    def on_success(self, n, new_cursor):
        if self.is_xhr:
            nugget = {"nugget_title": n.title,
                      "nugget_img": n.img,
                      "nugget_content": n.content,
                      "new_cursor": new_cursor    
                      }
            self.xhr_response.update(nugget)
            self.write(self.xhr_response)
