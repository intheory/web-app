#############################
# URL patterns.             #
# Author: Giorgos Eracleous #
#############################

from app.handlers import base, user, home

url_patterns = [
    ("/", home.HomePageHandler),
    ("/login", user.UserLoginHandler),
]
