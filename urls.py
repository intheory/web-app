#############################
# URL patterns.             #
# Author: Giorgos Eracleous #
#############################

from app.handlers import base,home, order

url_patterns = [
    ("/", home.HomePageHandler),
    ("/order", order.SelectItemsHandler),
]
