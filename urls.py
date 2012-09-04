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
    ("/learn/main", learn.ViewProgressHandler),
    ("/learn/section", learn.ViewSectionHandler),     
    ###########Practise pages hanlders##############
    
    ###########Backend hanlders##############
    ("/admin/users/moderator", admin.MakeModeratorHandler),
    ("/admin/users", admin.ViewUsersHandler),
    ("/admin/questions/add", admin.AddQuestionHandler),
    ("/admin/questions", admin.ViewQuestionsHandler),
    ("/admin", admin.ViewAdminPanelHandler),
]
