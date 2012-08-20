from app.handlers import base

class SelectItemsHandler(base.BaseHandler):
    '''
    Deals with the selection of food items
    '''
    def on_get(self):
        self.base_render("menu.html", items=[])

