#####
# One line summary.
#	This script creates a dictionary of 50 words in json format containing info on what users use these words. 
# 
# Usage:
#  	python get_word_json.py -> members_words_50.json 
# 
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

def findConnectedWords(token, bigrams): 
	# purpose: 	take a bigram list and return all words that are in the bigram with
	# 					the given token
	result = []  	
	for bigram in bigrams: 
		if bigram[0] == str(token): 
			result.append(bigram[1])
		if bigram[1] == str(token): 
			result.append(bigram[0])
	return result 

def processBio(bio):
	# this method processes a single biography of a user 
	import string
	raw = bio.lower().translate(string.maketrans("",""), string.punctuation)
	tokens = re.findall(r'\w+',raw)
	nonPunct = re.compile('.*[A-Za-z].*')                ## remove punctuation 
	filtered = [w for w in tokens if nonPunct.match(w)]  ## remove punctuation 
	tokens = filtered                                    ## remove punctuation 
	stops = ['wij', 'zijn', 'do', 'a','the','i', 'and', 'im', 'an', 'am', 
					 'aan', 'de', 'to', "\'", "it", "in", 'at', 'for', 'of', 'en', 
					 'on', 'is', 'with', 'we', 'are', 'if', 'you', 'op', 'long', 
					 'interested', 'from', 'im', 'about', 'more', 'my', 'van', 'looking',
					 'as', 'looking', 'working', 'currently', 'like', 'that', 'all', 
					 'love', 'be', 'but', 'this', 'have', 'also', 'years']     ## define stopwords
	corpus =[token for token in tokens if token not in stops]
	tokens = corpus 
	text = nltk.Text(tokens)
	fdist = nltk.FreqDist([w.lower() for w in text])
	return tokens

## first pull in all the member data that we are interested in 
member_json = [] 
for offset in range(0,11): 
	website 		= 'https://api.meetup.com/2/members?key=3ad7a28717926121647c7618457a2&sign=true&group_urlname=appsterdam&page=200&offset=' + str(offset) 
	new_members 	= json.loads(urllib.urlopen(website).read(), 'ISO-8859-1').items()[1][1]
	member_json.extend(new_members)

member_dict = {} 
words_dict = {} 
all_tokens = [] 

for member in member_json: 
	name 			= str(member['name'].encode('ascii','ignore'))
	member_id   	= str(member['id'])
	if 'bio' in member.keys(): 
		member_bio			= str(member['bio'].encode('ascii','ignore'))
		member_tokens 		= processBio(member_bio)
	else:
		member_bio 			= '' 
		member_tokens 		= [] 
	member_lat 		= member['lat'] 
	member_lon		= member['lon']
	member_dict[name] = {'name':name, 'member_id':member_id, 'member_bio':member_bio, 'member_lat':member_lat, 'member_lon':member_lon}
	bigrams 		= nltk.bigrams(member_tokens) 
	all_tokens = all_tokens + member_tokens
	for token in member_tokens: 
		connections = findConnectedWords(token, bigrams) 
		if token not in words_dict.keys(): 
			word_dict = {'name':str(token), 'freq':1, 'users':[name], 'connections':{}} 
			for word in connections: 
				word_dict['connections'][str(word)] = 1 
			words_dict[token] = word_dict
		else: 
			words_dict[token]['freq'] += 1
			if name not in words_dict[token]['users']: 
				words_dict[token]['users'].append(name)
			for word in connections: 
				if word not in words_dict[token]['connections']: 
					words_dict[token]['connections'][word] = 1 
				else: 
					words_dict[token]['connections'][word] += 1

# now for a selection of words 
# dict_200 = dict(sorted(words_dict.items(), key=lambda x: x[1])[len(words_dict)-200:len(words_dict)])
# dict_100 = dict(sorted(words_dict.items(), key=lambda x: x[1])[len(words_dict)-100:len(words_dict)])
dict_50  = dict(sorted(words_dict.items(), key=lambda x: x[1])[len(words_dict)- 50:len(words_dict)])

for key in dict_50:
		connections = []
		for connection in words_dict[key]['connections']: 
			new_dict = {} 
			new_dict['word'] = connection
			new_dict['freq'] = words_dict[key]['connections'][connection]
			connections.append(new_dict)
		dict_50[key]['connections'] = connections 

better_json_50 = []  
for key in dict_50.keys(): 
	new_dict = {} 
	new_dict['word'] = key 
	new_dict['content'] = dict_50[key]
	better_json_50.append(new_dict)

json_string = json.dumps(better_json_50)
myfile = open('members_words_50.json', 'wb')
myfile.write(json_string)
myfile.close() 

