from random import choice
import string
import os
from datetime import datetime  
from datetime import timedelta  
from mongoengine import connect
env = "ITENV" in os.environ and os.environ["ITENV"] or "dev"
if env=="prod":
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath("/www/virtualenv/intheory/src/app/model/content.py")))
    connect("intheory_dev")
else:
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath("/home/george/intheoryenv/intheory/src/app/model/content.py")))
    connect("intheory_dev")

os.sys.path.insert(0,parentdir) 
from model.coupons import Coupon
from optparse import OptionParser

if __name__ == "__main__":
    file_path = os.path.expanduser("~/" + os.path.join("intheorydata", "codes"))
    f = open(file_path+"/codes.txt", "r")

    while 1:
        code = f.readline().strip()        
        if len(code) == 0:
            break #EOF

        c = Coupon()
        c.code = code
        c.expiration_date = datetime.now() + timedelta(weeks=4)
        c.discount = 100
        c.redeemed = False
        c.save()
        