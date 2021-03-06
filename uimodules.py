################
## UI Modules ##
################

import tornado.web

class Question(tornado.web.UIModule):
    
    def render(self, test, timed):
        return self.render_string("ui-modules/question.html", test=test, timed=timed)

class Nugget(tornado.web.UIModule):
    
    def render(self, section, cursor, section_length):
        return self.render_string("ui-modules/nugget.html", section=section,
        													cursor=cursor,
        													section_length=section_length)
