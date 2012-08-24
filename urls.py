#############################
# URL patterns.             #
# Author: Giorgos Eracleous #
#############################

from app.handlers import base, user, home, admin

url_patterns = [
    ("/", home.HomePageHandler),
    ("/quiz/evaluate", home.EvaluateHomeQuizHandler),
    ("/login", user.UserLoginHandler),
    ###########Backend hanlders##############
    ("/admin/questions/add", admin.AddQuestionHandler),
    ("/admin/questions", admin.ViewQuestionsHandler),
    ("/admin", admin.ViewAdminPanelHandler),
]
