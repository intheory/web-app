'''
Created on 12 Sep 2012

@author: george

This module parses a txt file containing nuggets and saves them in the db.
'''
import os
from mongoengine import connect
from mongoengine.queryset import DoesNotExist
env = "ITENV" in os.environ and os.environ["ITENV"] or "dev"
if env=="prod":
	parentdir = os.path.dirname(os.path.dirname(os.path.abspath("/www/virtualenv/intheory/src/app/model/content.py")))
else:
	parentdir = os.path.dirname(os.path.dirname(os.path.abspath("/home/george/intheoryenv/intheory/src/app/model/content.py")))
os.sys.path.insert(0,parentdir) 
from model.content import Section, Nugget
connect("intheory_dev")

try:
	f = open("nuggets.txt", "r")

	while 1:
		content = f.readline().strip()
		if len(content) ==0:
			break # EOF
		print content
		title = f.readline().split('|')[1].strip()
		try:
			s = Section.objects(title=title).get()
		except DoesNotExist, e:
			s = Section()
			s.title = title	

		content = f.readline().strip()
		section_sub_title = f.readline().split('|')[1].strip()
		content = f.readline().strip()
		n = Nugget()
		n.section_sub_title =section_sub_title
		n.title = f.readline().split('|')[1].strip()
		n.content = f.readline().split('|')[1].strip()
		n.img = f.readline().split('|')[1].strip()
		s.nuggets.append(n)
		s.save()
	f.close()
except Exception, e:
	print e