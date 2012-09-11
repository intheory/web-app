'''
Created on 13 Nov 2011

@author: george

This module parses a txt file containing nuggets and saves them in the db.
'''
import app

f = open("nuggets.txt", "r")
content = f.readline()
while (content != "" ):
	content = content.strip()
	if content=="nugget":
		#n = Nugget()
		title = f.readline().split(',')[1].strip()
		content = f.readline().split(',')[1].strip()
		img = f.readline().split(',')[1].strip()
		section = f.readline().split(',')[1].strip()


f.close()