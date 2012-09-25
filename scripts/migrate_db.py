import os
from mongoengine import connect
env = "ITENV" in os.environ and os.environ["ITENV"] or "dev"
if env=="prod":
	parentdir = os.path.dirname(os.path.dirname(os.path.abspath("/www/virtualenv/intheory/src/app/model/content.py")))
	connect("intheory_dev")
else:
	parentdir = os.path.dirname(os.path.dirname(os.path.abspath("/home/george/intheoryenv/intheory/src/app/model/content.py")))
	connect("intheory_dev")

os.sys.path.insert(0,parentdir) 
from model.user import *

for u in User.objects:
	print u.types