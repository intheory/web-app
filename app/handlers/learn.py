import tornado
from app.handlers import base
from app.model.content import Section, MiniQuizQuestion#!@UnresolvedImport

class ViewSectionHandler(base.BaseHandler):
    '''
    Renders a section page.    
    '''
    @tornado.web.authenticated
    def on_get(self):
        sname = self.get_argument("name")
        #TODO: Get thge section from db 

class ViewLearnMainHandler(base.BaseHandler):
    '''
    Renders a page with the progress for each topic.    
    '''
    @tornado.web.authenticated
    def on_get(self):
        sections = Section.objects
        print sections
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