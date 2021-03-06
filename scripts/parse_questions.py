'''
Created on 13 Sep 2012

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
from model.content import Section, Nugget, Question
connect("intheory_dev")

try:
	file_path = os.path.expanduser("~/" + os.path.join("intheorydata", "content"))
	f = open(file_path+"/questions.txt", "r")
	while 1:
		content = f.readline().strip()
		print content

		if len(content) == 0:
			break #EOF

		title = f.readline().strip().rpartition("|")[2]
		try:
			s = Section.objects(title=title).get()
		except DoesNotExist, e:
			s = Section()
			s.title = title

		content = f.readline().strip()
		question_number = f.readline().strip()

		q = Question()
		q.question_number = question_number
		content = f.readline().strip()
		question = f.readline().strip()
		q.question = question
		content = f.readline().strip()

		while 1:
			option = f.readline().strip()

			if option == "answers":
				break
			q.options.append(option)
			
		answers = f.readline().strip()
		q.answer = [str(int(answer)-1) for answer in answers.split(',')]
		extract_tag = f.readline().strip()
		extract = f.readline().strip()
		q.extract = extract
		image = f.readline().strip()
		image_name = f.readline().strip()

		if image_name!="No":			
			q.image=image_name
		q.sid = str(s.id)
		q.save()

		s.questions.append(q)
		s.save()

		content = f.readline().strip()


	f.close()
except Exception, e:
	print e


# try:
# 	f = open("questions.txt", "r")
# 	while 1:
# 		content = f.readline().strip()
# 		if len(content) == 0:
# 			break #EOF

# 		title = f.readline().strip().rpartition("|")[2]
# 		s = Section(title="title")
# 		while True:
# 			content = f.readline().strip()
# 			if (content=="section"):
# 				break		
# 			question = f.readline().strip()
# 			q = Question()
# 			q.question = question
# 			content = f.readline().strip()
# 			while True:
# 				content = f.readline().strip()
# 				if content == "answers":
# 					break
# 				q.options.append(content)
# 			answers = f.readline().strip()
# 			q.answer = [str(int(answer)-1) for answer in answers.split(',')]
# 			extract_tag = f.readline().strip()
# 			extract = f.readline().strip()
# 			q.extract = extract
# 			image = f.readline().strip()
# 			image_exists = f.readline().strip()

# 			#Just for validation.
# 			print image_exists
# 			if image_exists != "no" and image_exists!="yes": 
# 				while 1:
# 					print q.question
# 					print image_exists; 
	
# 			if image_exists=="yes":			
# 				q.image="sample-sign.png"
# 			q.sid = str(s.id)
# 			q.save()

# 	f.close()
# except Exception, e:
# 	print e
