import tornado
from app.handlers import base

class ViewTermsAndConditionsHandler(base.BaseHandler):
    '''
    Renders the T&C page.    
    '''
    def on_get(self):
        self.base_render("landing/tc.html")

class ViewPrivacyPolicyHandler(base.BaseHandler):
	'''
	Renders the Privacy Policy page.    
	'''
	def on_get(self):
		self.base_render("landing/privacy.html")

class ViewAboutUsHandler(base.BaseHandler):
	'''
	Renders the About Us page.    
	'''
	def on_get(self):
		self.base_render("landing/about.html")     
