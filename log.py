'''
Implementation of logging for our app. Python logging is used to create a logger and its 
corresponding handler. The logs are stored in the database. 

@author: George Eracleous
Adapted from Alex Michael the Master 
'''
import logging, datetime

class CustomLogger(object):
	log_levels = {
                  'debug'    : logging.DEBUG,
                  'info'     : logging.INFO,
                  'warning'  : logging.WARNING,
                  'error'    : logging.ERROR,
                  'critical' : logging.CRITICAL
                  }

	def __init__(self, logger_name, log_level, log_collection_name, db):
		self.logger = logging.getLogger(logger_name)
		log_level = log_level = CustomLogger.log_levels.get(log_level, logging.DEBUG)
		self.logger.setLevel(log_level)
		self.logger.addHandler(logging.StreamHandler())
		self.logger.addHandler(DBHandler(log_collection_name, db))
        

	def get_logger(self):
		'''
		Returns the logger object
		'''
		return self.logger

class DBHandler(logging.Handler):
    
    def __init__(self, log_collection, db):
        ''' 
        Initializes the base Handler. Only messages having
        level INFO and higher will be stored.
        '''
        self.db = db
        self.log_collection = log_collection
        logging.Handler.__init__(self, logging.INFO)
   
		# create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		# add formatter to ch
        self.setFormatter(formatter)
   
    def emit(self, record):
        ''' 
        Overrides the base handler emit() method and
        writes the record in Mongo.
        '''
        self.db[self.log_collection].insert({
	                               'name'      : record.name,
	                               'filename'  : record.filename,
	                               'timestamp' : datetime.datetime.utcnow(),
	                               'level'     : record.levelname,
	                               'message'   : record.msg
	                               })