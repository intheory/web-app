'''
Created on 12 Sep 2012

@author: george

This module generates stats for our users. It does so in an aggregate manner.
User's identity is secure.
'''
import os
from prettytable import PrettyTable
from mongoengine import connect
from mongoengine.queryset import DoesNotExist
env = "ITENV" in os.environ and os.environ["ITENV"] or "dev"
if env=="prod":
	parentdir = os.path.dirname(os.path.dirname(os.path.abspath("/www/virtualenv/intheory/src/app/model/user.py")))
else:
	parentdir = os.path.dirname(os.path.dirname(os.path.abspath("/home/george/intheoryenv/intheory/src/app/model/user.py")))
os.sys.path.insert(0,parentdir) 
from model.user import User
from model.content import Section, MockTest, PractiseTest, HazardPerceptionTest
connect("intheory_dev")

total_sections = 0
total_practice = 0
total_mock = 0
total_hazard = 0
total_points = 0
total_questions_answered = 0
total_accuracy = 0 
total_progress = 0 

average_sections = 0
average_practice = 0
average_mock = 0
average_hazard = 0
average_points = 0
average_questions_answered = 0
average_accuracy = 0
average_progress = 0

detailed = PrettyTable(["User", "Sections", "Practice Tests", "Mock Tests", "Hazard Tests", "Points", "Accuracy", "Questions Answered", "Progress"])
for user in User.objects:
	sections = len(user.cursors.items())
	practice= len(PractiseTest.objects(user=user.id))
	mock = len(MockTest.objects(user=user.id))
	hazard = len(HazardPerceptionTest.objects(uid=user.id))
	stats = user.get_user_stats()
	progress = user.get_overall_progress()
	detailed.add_row([str(user.id), 
			   sections, 
			   practice, 
			   mock, 
			   hazard, 
			   stats['points'],
			   stats['accuracy'],
			   stats['total_questions_answered'],
			   progress ])

	total_sections += sections
	total_practice += practice
	total_mock += mock
	total_hazard += hazard
	total_points += stats['points']
	total_questions_answered += stats['total_questions_answered']
	total_accuracy += stats['accuracy']
	total_progress += progress

total_users = len(User.objects)

average = PrettyTable(["Sections", "Practice Tests", "Mock Tests", "Hazard Tests", "Points", "Accuracy", "Questions Answered", "Progress"])
average.add_row([ total_sections/float(total_users), 
				   total_practice/float(total_users), 
				   total_mock/float(total_users), 
				   total_hazard/float(total_users), 
				   total_points/float(total_users),
				   total_accuracy/float(total_users),
				   total_questions_answered/float(total_users),
				   total_progress/float(total_users) ])

file_path = os.path.expanduser("~/")
f = open(file_path+"/stats.txt", "w")	
f.write(detailed.get_string())
f.write("\n")
f.write(average.get_string())
