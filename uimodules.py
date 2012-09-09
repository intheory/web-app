################
## UI Modules ##
################

import tornado.web

class Question(tornado.web.UIModule):
    
    def render(self, test):
        return self.render_string("ui-modules/question.html", test=test)
