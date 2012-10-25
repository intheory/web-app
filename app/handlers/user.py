import tornado.auth, tornado.web
import functools
from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.user import *
from collections import defaultdict
from app.handlers.base import AjaxMessageException    
from tools import util
from app.model.content import Test, HazardPerceptionClip, HazardPerceptionTest

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

def has_paid(method):
    ''' 
    Decorator - Checks if the currently authenticated user is a paying user.
    If the user is authenticated and paying then we provide full access on the 
    website. If the user has not paid then we only allow them to preview a percentage
    of the page.
    '''
    def wrapper(self, *args, **kwargs):
        from app.handlers.learn import ViewSectionHandler, GetClipPageHandler
        from app.handlers.test import CreateNewTestHandler

        try:
            if self.current_user and self.current_user['has_paid']:
                return method(self, *args, **kwargs)
            elif isinstance(self, ViewSectionHandler) and self.current_user and len(self.current_user['cursors'].keys()) < self.settings['sections_limit']:
                #if the request is to see a new section and the user has not reached the limit allow it
                return method(self, *args, **kwargs)
            elif isinstance(self, CreateNewTestHandler) and self.current_user and len(Test.objects(user=str(self.current_user.id))) < self.settings['tests_limit']:
                #if the request is to start a new test and the user has not reached the limit allow it
                return method(self, *args, **kwargs)
            elif isinstance(self, GetClipPageHandler):
                #if this is the first time a user requests a new HAZARD test and the user has not reached the limit allow it
                return method(self, *args, **kwargs)
            elif isinstance(self, GetClipPageHandler) and self.current_user and len(HazardPerceptionTest.objects(uid=str(self.current_user.id))) < self.settings['clips_limit']:
                #if the request is to start a new HAZARD test and the user has not reached the limit allow it
                return method(self, *args, **kwargs)
            else:
                #else redirect them to the payment page
                self.redirect("/payment")
        except Exception, e:
            raise tornado.web.HTTPError(403)
    return wrapper

def has_paid2(method):
    ''' 
    Decorator - Checks if the currently authenticated user is a paying user.
    If the user is authenticated and paying then we provide full access on the 
    website. If the user has not paid then we only allow them to preview a percentage
    of the page. The difference between has_paid and has_paid2 is that the second one checks 
    if the user has watched two hazard perception videos.
    **USED FOR PPC**
    '''
    def wrapper(self, *args, **kwargs):
        from app.handlers.ppc import GetClipPageHandler
        try:
            if self.current_user and self.current_user['has_paid']:
                return method(self, *args, **kwargs)
            elif isinstance(self, GetClipPageHandler):
                #if this is the first time a user requests a new HAZARD test and the user has not reached the limit allow it
                return method(self, *args, **kwargs)
            elif isinstance(self, GetClipPageHandler) and self.current_user and len(HazardPerceptionTest.objects(uid=str(self.current_user.id))) < 2:
                #if the request is to start a new HAZARD test and the user has not reached the limit allow it
                return method(self, *args, **kwargs)
            else:
                #else redirect them to the payment page
                self.redirect("/payment")
        except Exception, e:
            raise tornado.web.HTTPError(403)
    return wrapper

class FBUserLoginHandler(base.BaseHandler, tornado.auth.FacebookGraphMixin):
    '''
    Handles the login for the Facebook user, returning a user object.
    '''
    @tornado.web.asynchronous
    def get(self):
        if self.env == "prod":
            URI = 'http://www.intheory.co.uk/login/fb'
        else:
            URI = 'http://localhost:8888/login/fb'

        next = self.get_argument("next", None)
        if next:
            self.set_secure_cookie("next", next)    

        access = self.get_argument("access", None)
        if access:
            self.set_secure_cookie("access", access)

        if self.get_argument("code", False):
            self.get_authenticated_user(
              redirect_uri=URI,
              client_id=self.settings["facebook_api_key"],
              client_secret=self.settings["facebook_secret"],
              code=self.get_argument("code"),
              callback=self.async_callback(                                                                                                 
                self._on_login))
            return
        self.authorize_redirect(redirect_uri=URI,
                                client_id=self.settings["facebook_api_key"],
                                extra_params={"scope": "email"})
    
    def _on_login(self, user):
        try:
            c_user = FacebookUser.objects(fb_id=user['id']).get()
        except DoesNotExist, e:   
            self.log.info("A new Facebook user is trying to login.")
            c_user = FacebookUser()
            c_user.access_token = user["access_token"]    
            c_user.profile_pic = str(user['picture']['data']['url'])   

            #Empty placeholders. The will be filled in when callback is called.
            c_user.username = ""
            c_user.first_name = ""
            c_user.last_name = ""
            c_user.fb_id = ""
            c_user.email = ""
            c_user.save()

            cb = functools.partial(self._save_user_profile, c_user)
            self.facebook_request("/me", access_token=c_user.access_token, callback=cb)
            
            cb = functools.partial(self._save_user_friends, c_user)
            self.facebook_request("/me/friends", access_token=c_user.access_token, callback=cb, fields='first_name,last_name,id,picture')
        except Exception, e:
            self.log.warning("Error while logging in user " + str(e))

        self.set_secure_cookie("access_token", c_user.access_token)
        self.set_secure_cookie("user_type", "fb")
        self.log.info("Facebook user with id " + str(c_user.id ) + " has successfully logged in.")

        access = self.get_secure_cookie("access")
        if access and access=="1":
            self.clear_cookie("access")
            c_user.has_paid = True   

        next = self.get_secure_cookie("next")
        if next:
            self.clear_cookie("next")
            self.redirect(next)   
        else:
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
        try:
            c_user.gender = response['gender']
        except Exception, e:
            self.log.warning("Error while retrieving FB user's gender" + str(e))
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

        self.authorize_redirect()

    def _on_auth(self, user):
        try:
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
                c_user.profile_pic = user['profile_image_url']
                c_user.save()

            self.set_secure_cookie("access_token", c_user.access_token)
            self.set_secure_cookie("user_type", "twitter")
            self.log.info("Twitter user with id " + str(c_user.id) + " has successfully logged in.")
            self.redirect('/')
        except Exception, e:
            self.log.warning("Error while authenticating Twitter user: " + str(e))


class UserLogoutHandler(base.BaseHandler):
    @tornado.web.authenticated
    def on_get(self):
        self.clear_cookie("access_token")
        self.clear_cookie("user_type")
        self.redirect('/')

class UserRegistrationHandler(base.BaseHandler):
    '''
    Handles a new user registraion. 
    '''
    def on_get(self):
        next = self.get_argument("next", None)
        if not next:
            next = "/dashboard"
        self.base_render("registration.html", next=next)

    def on_post(self):
        try:
            email = self.get_argument("email", None)
            username = self.get_argument("username", None)
            password = self.get_argument("password", None)
            msg = None

            #Validations
            if not username:
                msg = "You did not supply a username."
                return (None, msg)
            if not password:
                msg = "You did not supply a password."
                return (None, msg)
            if not email:
                msg = "You did not supply an email."
                return (None, msg)
            if not util.is_email(email):
                msg = "The email address is invalid."
                return (None, msg)
            if not util.is_name(username):
                msg = "The username must contain only letters."
                return (None, msg)
            if not util.check_length(password,"6","40"):
                msg = "The password must have at least 6 characters."
                return (None, msg)  

            new_user = IntheoryUser()

            #Some more validations
            if new_user.username_exists(username):
                msg = "Username not available"
                return (None, msg)
            if new_user.email_exists(email):
                msg = "Email already registered"
                return (None, msg)

            new_user.create_password(password)
            new_user.username = username.lower()
            #For intheory users we do not ask for first name or last name so we use username as an alias
            new_user.first_name = username
            new_user.last_name = ""
            new_user.email = email.lower()
            new_user.access_token = username
            new_user.save()
            return (new_user, None)

        except Exception, e:
            self.log.warning("Error while registering user with username " + username + ": " + str(e))

    def on_success(self, new_user, msg):
        if msg: #if something went wrong
            self.xhr_response.update({"msg": msg})        
            self.write(self.xhr_response)
        else:
            self.set_secure_cookie("access_token", new_user.access_token)
            self.set_secure_cookie("user_type", "intheory")
            self.log.info("Intheory user with id " + str(new_user.id ) + " has successfully registered.")
            self.write(self.xhr_response)

class IntheoryUserLoginHandler(base.BaseHandler):
    '''
    Handles the log in process of an Intheory user
    '''
    def on_post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        try:        
            if not username:
                raise DoesNotExist
            user = User.objects(username=username.lower()).get()
            if user.correct_password(password):
                self.set_secure_cookie("access_token", user.access_token)
                self.set_secure_cookie("user_type", "intheory")
                next = self.get_argument("next", None) or "/dashboard"
                self.log.info("Intheory user with id " + str(user.id ) + " has successfully logged in.")
                self.redirect(next)
            else:
                self.redirect("/login/options")
        except DoesNotExist:
            msg_username = "Username doesn't exist"
            self.redirect("/login/options")
             

