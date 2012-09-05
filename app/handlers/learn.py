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

        #Get all the nuggets associated with this section
        nuggets = Nugget.objects(section=sid)
        self.base_render("learn/learn-content.html", title=section.title, nuggets=nuggets)

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