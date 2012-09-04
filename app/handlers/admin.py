import tornado
from app.handlers import base, user
from app.model.content import Nugget, Section, Question, MiniQuizQuestion#!@UnresolvedImport
from app.model.user import *#!@UnresolvedImport

class ViewAdminPanelHandler(base.BaseHandler):
    '''
    Renders admin panel
    '''
    @user.moderator
    @tornado.web.authenticated
    def on_get(self):
        self.base_render("admin/admin-main.html")

class ViewQuestionsHandler(base.BaseHandler):
    '''
    Displays a list of questions
    '''
    
    @tornado.web.authenticated
    def on_get(self):
        self.base_render("admin/admin-questions.html")

class AddQuestionHandler(base.BaseHandler):
    '''
    Adds a new question
    '''
    @user.moderator 
    @tornado.web.authenticated
    def on_post(self):
        try:
            question = self.get_argument("question-inp", None)
            option1 = self.get_argument("option1-inp", None)
            option2 = self.get_argument("option2-inp", None)
            option3 = self.get_argument("option3-inp", None)
            option4 = self.get_argument("option4-inp", None)
            correct = [self.get_argument("0", None), self.get_argument("1", None),self.get_argument("2", None),self.get_argument("3", None)]
            type = self.get_argument("type", None)
            
            if type == "main":
                q = Question()
            elif type == "mini":
                q = MiniQuizQuestion()
            
            q.question = question
            q.options = [option1, option2, option3, option4]
            q.answer = [answer for answer in correct if answer != None]
            q.save()
        except Exception, e:
            print e

class ViewUsersHandler(base.BaseHandler):
    '''
    Displays a list of users
    '''
    @user.moderator 
    @tornado.web.authenticated
    def on_get(self):
        users = User.objects
        self.base_render("admin/admin-users.html", users=users)

class MakeModeratorHandler(base.BaseHandler):
    @user.moderator 
    @tornado.web.authenticated    
    def on_post(self):
        uid = self.get_argument("uid", None)
        user = User.objects(id = uid).get()
        user.toggle_moderator()
        return (user,) 

    def on_success(self, user):
        self.xhr_response.update({"moderator": user.moderator})  
        self.write(self.xhr_response)  

class ViewSectionsHandler(base.BaseHandler):
    '''
    Enables moderator to add a new section
    '''
    @user.moderator     
    @tornado.web.authenticated
    def on_get(self):
        sections = Section.objects
        self.base_render("admin/admin-sections.html", sections=sections)

class AddSectionHandler(base.BaseHandler):
    '''
    Adds a new section
    '''
    @user.moderator 
    @tornado.web.authenticated
    def on_post(self):
        try:
            title = self.get_argument("title-inp", None)
            s = Section()
            s.title = title
            s.save()
        except Exception, e:
            print e

class ViewNuggetsHandler(base.BaseHandler):
    '''
    Enables moderator to add a new nugget
    '''
    @user.moderator     
    @tornado.web.authenticated
    def on_get(self):
        self.base_render("admin/admin-nuggets.html", sections=Section.objects)

class AddNuggetHandler(base.BaseHandler):
    '''
    Adds a new nugget
    '''
    @user.moderator 
    @tornado.web.authenticated
    def on_post(self):
        try:
            title = self.get_argument("title-inp", None)
            content = self.get_argument("content-inp", None)
            img_name = self.get_argument("img-name-inp", None)
            section = self.get_argument("section", None)
            n = Nugget()
            n.title = title
            n.content = content
            n.img = img_name
            n.section = section
            n.save()
        except Exception, e:
            print e