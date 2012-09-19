'''
Created on 19 Sep 2012

@author: george

This module parses a txt file containing info about the hazard perception clips.
'''
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
from model.content import HazardPerceptionClip


try:
	f = open("clips.txt", "r")
	while 1:
		base_dir = f.readline().strip()
		if len(base_dir) ==0:
			break # EOF
		clip = HazardPerceptionClip()
		clip.base_dir = base_dir
		clip.title = f.readline().strip()
		while 1:
			hazard_point = f.readline().strip()
			if hazard_point=="end":
				break;
			clip.hazards.append(hazard_point)
		print clip.title
		print clip.base_dir
		print clip.hazards
		#clip.save()

	f.close()
except Exception, e:
	print e