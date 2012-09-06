import tornado
from app.handlers import base
from app.model.content import Section, Nugget, MiniQuizQuestion#!@UnresolvedImport

class ViewSectionHandler(base.BaseHandler):
    '''
    Renders a section page.    
    '''
    @tornado.web.authenticated
    def on_get(self):
        sid = self.get_argument("sid")
        #Get section object
        section = Section.objects(id=sid).get()

        #Get either the first nugget of the section or where the user left it off.
        nugget = Nugget.objects(id=section.first_nugget).get()
        if not nugget: #if we forgot to assign a first nugget we just pick the first one from db
            nugget = Nugget.objects()[0]
        self.base_render("learn/learn-content.html", title=section.title, nugget=nugget)

class ViewLearnMainHandler(base.BaseHandler):
    '''
    Renders a page with the progress for each topic.    
    '''
    @tornado.web.authenticated
    def on_get(self):
        sections = Section.objects
        self.base_render("learn/learn-main.html", sections= sections)

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
        pnid = self.get_argument("pnid", None)
        previous_nugget = Nugget.objects(id=pnid).get()
        return (previous_nugget,)

    def on_success(self, n):
        if self.is_xhr:
            nugget = {"nugget_title": n.title,
                      "nugget_previous": n.previous_nugget,
                      "nugget_next": n.next_nugget,    
                      "nugget_img": n.img,
                      "nugget_content": n.content
                      }
            self.xhr_response.update(nugget)
            self.write(self.xhr_response)

class GetNextNuggetHandler(base.BaseHandler):
    '''
    Gets the next nugget
    '''
    def on_get(self):
        nnid = self.get_argument("nnid", None)
        next_nugget = Nugget.objects(id=nnid).get()
        return (next_nugget,)

    def on_success(self, n):
        if self.is_xhr:
            nugget = {"nugget_title": n.title,
                      "nugget_previous": n.previous_nugget,
                      "nugget_next": n.next_nugget,    
                      "nugget_img": n.img,
                      "nugget_content": n.content
                      }
            self.xhr_response.update(nugget)
            self.write(self.xhr_response)
