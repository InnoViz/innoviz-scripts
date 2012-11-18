#####
# One line summary.
#	This script creates a json dict of appsterdam members. 
# 
# Usage:
#  	python get_word_json.py -> members_words_50.json 
# 
# small bug: API limit of 200 ... so we wont get all data in one go  
# 					 you can run this in ipython though and it should work just fine 
#####

import nltk
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
import re
from collections import Counter
import sys 
import itertools 
import string 
import csv 
import urllib
import json 

## first pull in all the member data that we are interested in 
member_json = [] 
for offset in range(0,11): 
	website 		= 'https://api.meetup.com/2/members?key=3ad7a28717926121647c7618457a2&sign=true&group_urlname=appsterdam&page=200&offset=' + str(offset) 
	new_members 	= json.loads(urllib.urlopen(website).read(), 'ISO-8859-1').items()[1][1]
	member_json.extend(new_members)

json_string = json.dumps(member_json)
myfile = open('members.json', 'wb')
myfile.write(json_string)
myfile.close()
