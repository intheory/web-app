####################################
# Tornado App Launcher.            #
# Author: Giorgos Eracleous  	   #
# Acknowledgement: Alexis Michael  #
####################################

import ConfigParser #@UnresolvedImport
import environment #@UnusedImport
import tornado.web, os, pymongo, uimodules
import app.deps
from log import CustomLogger
from urls import url_patterns
from dependencies import css_deps, js_deps
from mongoengine import connect #@UnresolvedImport
from optparse import OptionParser #@UnresolvedImport
from app.model.user import *

class Intheory(tornado.web.Application):
    def __init__(self, env, port, config_file):
	self.APP_NAME = "intheory-" + str(port)
	
        if env == "prod":
            facebook_api_key = "486623404681319"
            facebook_secret = "4049a6a2d8dd781bbfb4a1b849869113"
        else:
            facebook_api_key = "387574291313993"
            facebook_secret = "37c0042436064296a4c17242088cd1fe"

    	settings = {
                        'static_path'   : "static",
                        'template_path' : "templates",
                        'cookie_secret' : "aKlRsPkySWyOqByxAQfLsKMbEAKj3ErRtg1RgkBUQ6E=noteslib",
                        'login_url'     : "/login", #landing page if user is not authenticated
                        'xsrf_cookies'  : True,
                        'autoescape'    : "xhtml_escape",
                        'facebook_api_key': facebook_api_key,
                        'facebook_secret': facebook_secret,
                        'twitter_consumer_key':"bJ5IIoEfSuuAWvfBM0Q",
                        'twitter_consumer_secret':"GZZhvI0AP6kimS0IwsD401RfE2IVrXTatBMpnI4a0",
                        'ui_modules'     : uimodules
                        }

    	config = ConfigParser.RawConfigParser()
        config.read(config_file)

        ############################
        #  Databse configuration   #
        ############################
        
        db_host = config.get(env, "db_host") or "localhost"
        db_name = config.get(env, "db_name") or "intheory_db" + "_" + env
        db_user = config.get(env, "db_user")
        db_pass = config.get(env, "db_pass")

	if env == "prod" and db_user and db_pass:
            connect(db_name, host=db_host, username=db_user, password=db_pass)
        else:
            connect(db_name, host=db_host)
        
        conn = pymongo.Connection(host=db_host)

	if hasattr(conn, db_name):
            db = getattr(conn, db_name)
            if env == "prod" and db_user and db_pass:
                db.authenticate(db_user, db_pass)
            # Create some capped collections..
            if "system.profile" not in db.collection_names():
                db.create_collection("system.profile", capped=True, size=50000000, max=300000)
            db.set_profiling_level(pymongo.ALL)

        ############################################
        ## Configure CSS and JS dependency loader ##
        ############################################
        
        deps = app.deps.ScriptDeps().registerDep(css_deps).registerDep(js_deps)

        ########################################################
        ## Logging setup. ##
        ########################################################	    
        log_level = db_host = config.get(env, "log_level") or "debug"
        log_db_collection = db_host = config.get(env, "log_db_collection") or "Log"
        cl = CustomLogger(self.APP_NAME, log_level, log_db_collection, db)

        ########################################################
        ## Initialize references to application-wide modules. ##
        ########################################################
        self.user_types = {"twitter": TwitterUser, "fb": FacebookUser}    
        self.db   = db
        self.deps = deps
        self.env  = env
        self.log = cl.get_logger()
	    
        self.log.info("Server started successfully.")

        tornado.web.Application.__init__(self, url_patterns, **settings)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-p", type="int", dest="port", help="Server port.")
    parser.add_option("-c", type="string", dest="config", help="Config file location.")
    options, args = parser.parse_args()
    
    env = "ITENV" in os.environ and os.environ["ITENV"] or "dev"
    config_file = options.config or os.path.join("config", "config.default")
    config = ConfigParser.RawConfigParser()
    config.read(config_file)
    port = int(options.port or config.get(env, "port") or 8888)
    Intheory(env, port, config_file).listen(port)
    tornado.ioloop.IOLoop.instance().start()
