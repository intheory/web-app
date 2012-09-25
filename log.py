'''
Implementation of logging for our app. Python logging is used to create a logger and its 
corresponding handler. The logs are stored in the database. 

@author: George Eracleous
'''
import logging 

class CustomLogger(object):

	def __init__(self, logger_name, log_level, log_collection_name, db):
		self.logger = logging.getLogger(logger_name)

	def get_logger(self):
		return self.logger