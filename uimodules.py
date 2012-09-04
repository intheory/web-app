################
## UI Modules ##
################

import tornado.web

class Question(tornado.web.UIModule):
    
    def render(self, question):
        return self.render_string("ui-modules/question.html", question=question)
