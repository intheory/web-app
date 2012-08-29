#############################
# URL patterns.             #
# Author: Giorgos Eracleous #
#############################

from app.handlers import base, user, home, admin,  dashboard

url_patterns = [
    ("/", home.HomePageHandler),
    ("/quiz/evaluate", home.EvaluateHomeQuizHandler),
    ("/login", user.UserLoginHandler),
    ("/logout", user.UserLogoutHandler),
    ###########Dashboard hanlders##############
    ("/dashboard", dashboard.ViewDashBoardHandler),
    ###########Backend hanlders##############
    ("/admin/questions/add", admin.AddQuestionHandler),
    ("/admin/questions", admin.ViewQuestionsHandler),
    ("/admin", admin.ViewAdminPanelHandler),
]
