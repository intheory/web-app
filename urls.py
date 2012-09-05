#############################
# URL patterns.             #
# Author: Giorgos Eracleous #
#############################

from app.handlers import base, user, home, admin,  dashboard, learn

url_patterns = [
    ("/", home.HomePageHandler),
    ("/quiz/evaluate", home.EvaluateHomeQuizHandler),
    ("/login", user.UserLoginHandler),
    ("/logout", user.UserLogoutHandler),
    ###########Dashboard hanlders##############
    ("/dashboard", dashboard.ViewDashBoardHandler),
    ###########Learning pages hanlders##############
    ("/learn/main", learn.ViewLearnMainHandler),
    ("/learn/section", learn.ViewSectionHandler),  
    ("/learn/get-previous-nugget", learn.GetPreviousNuggetHandler),
    ###########Practise pages hanlders##############
    
    ###########Backend hanlders##############
    ("/admin/users/moderator", admin.MakeModeratorHandler),
    ("/admin/users", admin.ViewUsersHandler),
    ("/admin/questions/add", admin.AddQuestionHandler),
    ("/admin/questions", admin.ViewQuestionsHandler),
    ("/admin/sections/add", admin.AddSectionHandler),       
    ("/admin/sections", admin.ViewSectionsHandler),
    ("/admin/nuggets/rearrange", admin.RearrangeNuggetsHandler), 
    ("/admin/nuggets/get", admin.GetNuggetsHandler),
    ("/admin/nuggets/add", admin.AddNuggetHandler),        
    ("/admin/nuggets", admin.ViewNuggetsHandler),        
    ("/admin", admin.ViewAdminPanelHandler),
]
