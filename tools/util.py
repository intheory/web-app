'''
This file contains utility functions.

@author: George Eracleous
'''
import re

def is_name(data):
    '''
    Allows only names
    ''' 
    return re.match(u'^[a-zA-Z "\u0380-\u03DC"]{1,40}$', data)

def is_numeric(data):
    '''
    Allows only digits
    ''' 
    return re.match("^[0-9]+$", data)

def is_email(data):
    '''
    Check if it's a valid email address
    ''' 
    return re.match("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$", data)

def check_length(data, min, max):
    '''
    Check the length of a string
    ''' 
    return re.match(".{"+min+","+max+"}$", data)