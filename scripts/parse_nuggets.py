'''
Created on 13 Nov 2011

@author: george

This module parses a txt file containing nuggets and saves them in the db.
'''
import os
from mongoengine import connect
parentdir = os.path.dirname(os.path.dirname(os.path.abspath("/home/george/intheoryenv/intheory/src/app/model/content.py")))
os.sys.path.insert(0,parentdir) 
from model.content import Section, Nugget
connect("intheory_dev")

f = open("nuggets.txt", "r")
content = f.readline().strip()
while 1:
	if len(content) ==0:
		break # EOF

	if content=="section":
		s_title = f.readline().split(',')[1].strip()
		s = Section()
		s.title = s_title
		content = f.readline().strip()
		while (content=="nugget" and len(content)!=0):
			n = Nugget()
			n.title = f.readline().split(',')[1].strip()
			n.content = f.readline().split(',')[1].strip()
			n.img = f.readline().split(',')[1].strip()
			s.nuggets.append(n)
			content = f.readline().strip()
		s.save()
f.close()