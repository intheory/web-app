from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.user import *
import tornado.auth, tornado.web
import functools
    
def moderator(method):
    ''' 
    Decorator - Checks if the currently authenticated user is a moderator.
    Intended to be used together with tornado.web.authenticated in places
    where moderator access is required.
    '''
    def wrapper(self, *args, **kwargs):
        try:
            if self.current_user and self.current_user['moderator']:
                return method(self, *args, **kwargs)
            else:
                raise tornado.web.HTTPError(403)
        except:
            raise tornado.web.HTTPError(403)
    return wrapper

class UserLoginHandler(base.BaseHandler, tornado.auth.FacebookGraphMixin):
    '''
    Handles the login for the Facebook user, returning a user object.
    '''
    
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("code", False):
            self.get_authenticated_user(
              redirect_uri='http://www.intheory.co.uk/login',
              client_id=self.settings["facebook_api_key"],
              client_secret=self.settings["facebook_secret"],
              code=self.get_argument("code"),
              callback=self.async_callback(                                                                                                 
                self._on_login))
            return
        elif self.get_secure_cookie('email'):
            self.redirect('/circles/create')
            return
        
        self.authorize_redirect(redirect_uri='http://www.intheory.co.uk/login',
                                client_id=self.settings["facebook_api_key"],
                                extra_params={"scope": "email"})
    
    def _on_login(self, user):
        try:
            c_user = FacebookUser.objects(fb_id=user['id']).get()
        except DoesNotExist, e:   
            self.log.info("A new Facebook user is trying to login.")
            c_user = FacebookUser()
            c_user.access_token = user["access_token"]        
            cb = functools.partial(self._save_user_profile, c_user)
            self.facebook_request("/me", access_token=c_user.access_token, callback=cb)
            
            cb = functools.partial(self._save_user_friends, c_user)
            self.facebook_request("/me/friends", access_token=c_user.access_token, callback=cb, fields='first_name,last_name,id,picture')
        
        self.set_secure_cookie("access_token", c_user.access_token)
        self.set_secure_cookie("user_type", "fb")
        self.log.info("Facebook user " + c_user.first_name + " " + c_user.last_name  + " has successfully logged in.")
        self.redirect("/dashboard")   

    
    def _save_user_profile(self, c_user, response):
        '''
        This callback receives "user" which is the response from the API and contains the info for a user's profile.
        '''
        if not response:
            raise tornado.web.HTTPError(500, "Facebook authentication failed.")

        c_user.first_name = response['first_name']
        c_user.last_name = response['last_name']
        c_user.email = response['email'] 
        c_user.username = response['username']
        c_user.gender = response['gender']
        c_user.locale = response['locale']
        c_user.fb_id = response['id']
        c_user.save()    

    def _save_user_friends(self, c_user, response):
        '''
        This callback receives the response from the API that contains user's friends.
        '''
        if not c_user:
            raise tornado.web.HTTPError(500, "Facebook authentication failed.")
        friends = response['data']
        for friend in friends:
            uf = UserFriend()
            uf.first_name = friend['first_name']
            uf.last_name = friend['last_name']
            uf.profile_pic = friend['picture']['data']['url']
            uf.fb_id = friend['id']
            c_user.friends.append(uf)
        c_user.save()
    

class TwitterUserLoginHandler(base.BaseHandler, tornado.auth.TwitterMixin):
    '''
    Handles the login for the Twitter user, returning a user object.
    '''
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return

        #self.authorize_redirect(callback_uri='http://127.0.0.1:8888/login/twitter')
        self.authorize_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Twitter auth failed")
       
        try:
            c_user = TwitterUser.objects(twitter_id=str(user['id'])).get()
        except DoesNotExist, e:
            c_user = TwitterUser()
            name = user['name'].split()
            c_user.first_name = name[0]
            if len(name)>1:
                c_user.last_name = name[1]
            else:
                c_user.last_name = ""
            c_user.username = user['username']
            c_user.access_token = user['access_token']['secret']
            c_user.twitter_id = str(user['id'])
            c_user.save()

        self.set_secure_cookie("access_token", c_user.access_token)
        self.set_secure_cookie("user_type", "twitter")
        self.log.info("Twitter user " + c_user.first_name + " " + c_user.last_name  + " has successfully logged in.")
        self.redirect('/')


class UserLogoutHandler(base.BaseHandler):
    @tornado.web.authenticated
    def on_get(self):
        try: 
            
            self.clear_cookie("access_token")
            self.clear_cookie("user_type")
            self.redirect('/')
        except Exception, e:
            print e