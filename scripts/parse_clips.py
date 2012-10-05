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
from model.content import HazardPerceptionClip, HazardPoint

HazardPerceptionClip.drop_collection()
try:
	file_path = os.path.expanduser("~/" + os.path.join("intheorydata", "content"))
	f = open(file_path+"/clips.txt", "r")
	while 1:
		base_dir = f.readline().strip()
		if len(base_dir) ==0:
			break # EOF
		clip = HazardPerceptionClip()
		clip.base_dir = base_dir
		clip.clip_name = f.readline().strip()
		clip.solution_clip_name = f.readline().strip()

		hp = HazardPoint()
		hp.start = int(f.readline().strip())
		hp.end = int(f.readline().strip())
		clip.hazards.append(hp)
		clip.save()

	f.close()
except Exception, e:
	print e