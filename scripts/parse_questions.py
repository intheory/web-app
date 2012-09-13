'''
Created on 13 Sep 2012

@author: george

This module parses a txt file containing nuggets and saves them in the db.
'''
import os
from mongoengine import connect
parentdir = os.path.dirname(os.path.dirname(os.path.abspath("/home/george/intheoryenv/intheory/src/app/model/content.py")))
os.sys.path.insert(0,parentdir) 
from model.content import Section, Nugget, Question
connect("intheory_dev")

try:
	f = open("questions.txt", "r")
	while 1:
		content = f.readline().strip()
		if len(content) == 0:
			break #EOF

		if content == "section":
			title = f.readline().strip().rpartition("|")[2]
			s = Section(title="title")
			content = f.readline().strip()
			while (content!="section"):
				question = f.readline().strip()
				q = Question()
				q.question = question
				content = f.readline().strip()
				if content == "options":
					while True:
						content = f.readline().strip()
						if content == "extract":
							break
						q.options.append(content)
				extract = f.readline().strip()
				q.extract = extract
				image = f.readline().strip()
				image_exists = f.readline().strip()
				print image_exists
				if image_exists=="yes":
					pass#TODO:save image's name
				q.sid = str(s.id)
				q.answer.append("0")#TODO: Add actual answer/s
				q.save()
				content = f.readline().strip()
		content = f.readline().strip()
	f.close()
except Exception, e:
	print e
