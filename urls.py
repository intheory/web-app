#############################
# URL patterns.             #
# Author: Giorgos Eracleous #
#############################
import tornado, os
from app.handlers import base, user, test, home, admin,  dashboard, learn, landing, practise, payments, ppc

url_patterns = [
    ("/", home.HomePageHandler),
    ("/login/options", home.LoginScreenHandler),
    ("/login/twitter", user.TwitterUserLoginHandler),
    ("/login/fb", user.FBUserLoginHandler),
    ("/login/intheory", user.IntheoryUserLoginHandler),
    ("/register", user.UserRegistrationHandler),
    ("/logout", user.UserLogoutHandler),
    ###########Dashboard hanlders##############
    ("/dashboard/remove-msg", dashboard.RemoveDashBoardMsgHandler),
    ("/dashboard", dashboard.ViewDashBoardHandler),
    ###########Learning pages hanlders##############
    ("/learn/main", learn.ViewLearnMainHandler),
    ("/learn/section", learn.ViewSectionHandler),  
    ("/learn/get-question", learn.GetQuestionHandler),
    ("/learn/get-previous-nugget", learn.GetPreviousNuggetHandler),
    ("/learn/get-next-nugget", learn.GetNextNuggetHandler),
    ("/learn/hazard/evaluate", learn.EvaluateHazardPerceptionHandler),
    ("/learn/hazard/clip/intro", learn.GetIntroClipPageHandler),    
    ("/learn/hazard/clip", learn.GetClipPageHandler),    
    ("/learn/hazard", learn.GetHazardPerceptionHandler),    
    ###########Practice hanlders##############
    ("/practice/main", practise.ViewPracticeMainHandler),
    ###########Mock test hanlders##############
    ("/test/new", test.CreateNewTestHandler),
    ("/test/get-new", test.GetNewTestHandler),
    ("/test/get-next-after-wrong", test.GetNextAfterWrongQuestionHandler),
    ("/test/get-next", test.GetNextQuestionHandler),
    ("/test/get-previous", test.GetPreviousQuestionHandler),
    ("/test/delete", test.DeleteTestHandler),
    ###########Backend hanlders##############
    ("/admin/feedback", admin.SubmitFeedbackHandler),
    ("/admin/coupons", admin.ViewCouponsHandler),
    ("/admin/logs", admin.ViewLogsHandler),
    ("/admin/users/free", admin.GiveFreeAccessHandler),
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
    ###########Payment hanlders##############
    ("/payment/do", payments.DoPaymentHandler),
    ("/payment/redirect", payments.RedirectToPayPalHandler),
    ("/payment/redeem-coupon", payments.RedeemCouponHandler),
    ("/payment", payments.ViewPaymentPageHandler),
    ###########PPC hanlders##############
    ("/pt-welcome", ppc.PT1Handler),
    ("/pt-home", ppc.PT2Handler),
    ("/hp-welcome", ppc.HP1Handler),
    ("/hp-home", ppc.HP2Handler),
    ("/learn/hazardboard", ppc.GetTwoClicksPaywallDashboardHandler),    
    ("/learn/hazardboard/clip/intro", ppc.GetIntroClipPageHandler),    
    ("/learn/hazardboard/clip", ppc.GetClipPageHandler),    
    ("/learn/hazardboard/evaluate", ppc.EvaluateHazardPerceptionHandler),
    ###########Static files handlers################
    ("/obj/img/questions/(.*)", tornado.web.StaticFileHandler, {"path": os.path.expanduser("~/" + os.path.join("intheorydata", "imgs/questions"))}),
    ("/obj/img/nuggets/(.*)", tornado.web.StaticFileHandler, {"path": os.path.expanduser("~/" + os.path.join("intheorydata", "imgs/nuggets"))}),    
    ("/obj/img/(.*)", tornado.web.StaticFileHandler, {"path": os.path.expanduser("~/" + os.path.join("intheorydata", "imgs"))}),
    ("/obj/video/(.*)", tornado.web.StaticFileHandler, {"path": os.path.expanduser("~/" + os.path.join("intheorydata", "videos"))}),
]
