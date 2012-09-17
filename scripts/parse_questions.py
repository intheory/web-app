'''
Created on 13 Sep 2012

@author: george

This module parses a txt file containing nuggets and saves them in the db.
'''
import os
from mongoengine import connect
#parentdir = os.path.dirname(os.path.dirname(os.path.abspath("/home/george/intheoryenv/intheory/src/app/model/content.py")))
parentdir = os.path.dirname(os.path.dirname(os.path.abspath("/www/virtualenv/intheory/src/app/model/content.py")))
os.sys.path.insert(0,parentdir) 
from model.content import Section, Nugget, Question
connect("intheory_dev")

try:
	f = open("questions.txt", "r")
	while 1:
		content = f.readline().strip()
		if len(content) == 0:
			break #EOF

		title = f.readline().strip().rpartition("|")[2]
		s = Section(title="title")
		while True:
			content = f.readline().strip()
			if (content=="section"):
				break		
			question = f.readline().strip()
			q = Question()
			q.question = question
			content = f.readline().strip()
			while True:
				content = f.readline().strip()
				if content == "answers":
					break
				q.options.append(content)
			answers = f.readline().strip()
			q.answer = [str(int(answer)-1) for answer in answers.split(',')]
			extract_tag = f.readline().strip()
			extract = f.readline().strip()
			q.extract = extract
			image = f.readline().strip()
			image_exists = f.readline().strip()

			#Just for validation.
			print image_exists
			if image_exists != "no" and image_exists!="yes": 
				while 1:
					print q.question
					print image_exists; 
	
			if image_exists=="yes":			
				q.image="sample-sign.png"
			q.sid = str(s.id)
			q.save()

	f.close()
except Exception, e:
	print e
