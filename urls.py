#############################
# URL patterns.             #
# Author: Giorgos Eracleous #
#############################
import tornado, os
from app.handlers import base, user, test, home, admin,  dashboard, learn, landing

url_patterns = [
    ("/", home.HomePageHandler),
    ("/quiz/evaluate", home.EvaluateHomeQuizHandler),
    ("/login/options", home.LoginScreenHandler),
    ("/login/twitter", user.TwitterUserLoginHandler),
    ("/login", user.UserLoginHandler),
    ("/logout", user.UserLogoutHandler),
    ###########Dashboard hanlders##############
    ("/dashboard", dashboard.ViewDashBoardHandler),
    ###########Learning pages hanlders##############
    ("/learn/main", learn.ViewLearnMainHandler),
    ("/learn/section", learn.ViewSectionHandler),  
    ("/learn/get-question", learn.GetQuestionHandler),
    ("/learn/get-previous-nugget", learn.GetPreviousNuggetHandler),
    ("/learn/get-next-nugget", learn.GetNextNuggetHandler),
    ("/learn/hazard/evaluate", learn.EvaluateHazardPerceptionHandler),
    ("/learn/hazard", learn.GetHazardPerceptionHandler),    
    ###########Mock test hanlders##############
    ("/test/new", test.CreateNewTestHandler),
    ("/test/get-new", test.GetNewTestHandler),
    ("/test/get-next", test.GetNextQuestionHandler),
    ("/test/get-previous", test.GetPreviousQuestionHandler),
    ("/test/delete", test.DeleteTestHandler),
    ###########Backend hanlders##############
    ("/admin/feedback", admin.SubmitFeedbackHandler),
    ("/admin/logs", admin.ViewLogsHandler),
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
    ###########Landing pages hanlders##############
    ("/landing/terms", landing.ViewTermsAndConditionsHandler),
    ("/landing/privacy", landing.ViewPrivacyPolicyHandler),
    ("/landing/about", landing.ViewAboutUsHandler),
    ###########Static files handlers################
    ("/obj/img/question/(.*)", tornado.web.StaticFileHandler, {"path": os.path.expanduser("~/" + os.path.join("intheorydata", "imgs/questions"))}),
    ("/obj/img/nugget/(.*)", tornado.web.StaticFileHandler, {"path": os.path.expanduser("~/" + os.path.join("intheorydata", "imgs/nuggets"))}),
    ("/obj/img/(.*)", tornado.web.StaticFileHandler, {"path": os.path.expanduser("~/" + os.path.join("intheorydata", "imgs"))}),
    ("/obj/video/(.*)", tornado.web.StaticFileHandler, {"path": os.path.expanduser("~/" + os.path.join("intheorydata", "videos"))}),
]
