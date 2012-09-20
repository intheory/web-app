#############################
# URL patterns.             #
# Author: Giorgos Eracleous #
#############################

from app.handlers import base, user, test, home, admin,  dashboard, learn, landing

url_patterns = [
    ("/", home.HomePageHandler),
    ("/quiz/evaluate", home.EvaluateHomeQuizHandler),
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
    ###########Practise pages hanlders##############

    ###########Mock test hanlders##############
    ("/test/new", test.GetNewTestHandler),
    ("/test/evaluate", test.EvaluateTestQuestionHandler),
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
    ###########Landing pages hanlders##############
    ("/landing/terms", landing.ViewTermsAndConditionsHandler),
    ("/landing/privacy", landing.ViewPrivacyPolicyHandler),
    ("/landing/about", landing.ViewAboutUsHandler),
]
