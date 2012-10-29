'''
Created on 12 Sep 2012

@author: george

This module generates stats for our users. 
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

blacklist = ["guypengelley", "matt.simmonds.376", "tomwoolway", "zahid.mitha", "kitbrennan90","lbeischer", "dan.edge.39", "johnking7", "james.hennessey.7", "jon.wright.3367", "simon.worthington", "yasmin",
"zefi.hh", "shoaib.noor1", "alicebentinck", "davekmason", "pambose", "ewan.marshall", "giorgos.eracleous", "i.k.lewis", "nilu.satharasinghe", "nik.adhia", "gmakkoulis", "humphrey.flowerdew", "shoaib.noor1",
 "andrew.jervis", "geracleous", "divomas", "kronosmes", "jerry", "ppapageorgiou", "jerrydelmissier", "matt.p.clifford", "rashid.mansoor", "The0s", "davidmason", "jerrya", "paymentstest", "zahida", "kit", 
 "elia.videtta", "isabel.be.58", "emilysophiebrooke", "varun.kapur.9", "don.nightingale.92", "levng", "vivian.chan.9480111", "al.frankl", "aditya.kasliwal", "henri.cammiade", "derrick.crentsil", "john smith", "codetest"
 "masonova", "wicksy", "zahid", "billy.sowden", "petesmithy0", "tomwoolway", "emilios.nicolaou", "henri.cammiade"]

total_pageviews = 0
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

total_people_with_zero_pageviews = 0

detailed = PrettyTable(["User", "Sections", "Practice Tests", "Mock Tests", "Hazard Tests", "Points", "Accuracy", "Questions Answered", "Progress", "Pageviews"])
for user in User.objects.order_by("-points"):
	if user.username not in blacklist: 
		sections = len(user.cursors.items())
		practice= len(PractiseTest.objects(user=str(user.id)))
		mock = len(MockTest.objects(user=str(user.id)))
		hazard = len(HazardPerceptionTest.objects(uid=str(user.id)))
		stats = user.get_user_stats()
		progress = user.get_overall_progress()

		#pageviews are an estimate of ghow many pages they've seen based on the number of completed tests and nuggets
		nuggets = 0
		for item in user.cursors.items():
			nuggets += int(item[1]) 
		pageviews = practice*20 + mock*50 + nuggets 
		detailed.add_row([str(user.username), 
				   sections, 
				   practice, 
				   mock, 
				   hazard, 
				   stats['points'],
				   stats['accuracy'],
				   stats['total_questions_answered'],
				   progress,
				   pageviews
				    ])

		total_sections += sections
		total_practice += practice
		total_mock += mock
		total_hazard += hazard
		total_points += stats['points']
		total_questions_answered += stats['total_questions_answered']
		total_accuracy += stats['accuracy']
		total_progress += progress
		total_pageviews += pageviews

total_users = len(User.objects) - len(blacklist) - total_people_with_zero_pageviews

average = PrettyTable(["Sections", "Practice Tests", "Mock Tests", "Hazard Tests", "Points", "Accuracy", "Questions Answered", "Progress", "Pageviews"])
average.add_row([ total_sections/float(total_users), 
				   total_practice/float(total_users), 
				   total_mock/float(total_users), 
				   total_hazard/float(total_users), 
				   total_points/float(total_users),
				   total_accuracy/float(total_users),
				   total_questions_answered/float(total_users),
				   total_progress/float(total_users),
				   total_pageviews/float(total_users) ])

file_path = os.path.expanduser("~/")
f = open(file_path+"/stats.txt", "w")	
f.write(detailed.get_string())
f.write("\n")
f.write(average.get_string())
