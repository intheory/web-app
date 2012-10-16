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

def GenPasswd():
    chars = string.letters + string.digits
    for i in range(8):
        newpasswd = newpasswd + choice(chars)
    return newpasswd

def GenPasswd2(length=8, chars=string.letters[26:] + string.digits):
    return ''.join([choice(chars) for i in range(length)])

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-c", type="int", dest="coupons", help="Number of coupons to be generated.")
    parser.add_option("-d", type="int", dest="discount", help="The discount for these coupons.")
    options, args = parser.parse_args()

    codes = []
    for i in xrange(options.coupons):
        new_code = GenPasswd2(8)
        while len(Coupon.objects(code=new_code)) > 0: #Code already exists in db 
            new_code =GenPasswd2(8)
        c = Coupon()
        c.code = new_code
        codes.append(new_code)
        c.expiration_date = datetime.now() + timedelta(weeks=4)
        c.discount = options.discount
        c.redeemed = False
        c.save()
        
    f = open('/home/george/Desktop/codes.txt', 'w')
    for code in codes:
        f.write(code)
        f.write("\n")