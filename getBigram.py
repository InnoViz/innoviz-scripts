## appsterdam website data 

## usage: call this script followed by a text file 
## 		  the script will then create a .csv file with all bigrams and their weight in the file 
##        the cript is aimed at showing info from the appsterdam member profiles 

## example calls: 
## 		  $ python getBigram.py example.txt 
## 		  $ python getBigram.py member_descripion 

## prerequisites: 
## 		python 2.7.3 
## 		nltk package 

## output : a csv file containing all the bigrams and the frequency  
##  		a csv file containing the frequency of each word  

import nltk
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
import re
from collections import Counter
import sys 
import itertools 
import csv 

## dump all the text from a source in a text file 
print sys.argv[1] 



f = open(sys.argv[1])
raw = f.read()
raw = raw.lower()
tokens = nltk.word_tokenize(raw)
nonPunct = re.compile('.*[A-Za-z].*')                ## remove punctuation 
filtered = [w for w in tokens if nonPunct.match(w)]  ## remove punctuation 
tokens = filtered                                    ## remove punctuation 
stops = ['wij', 'zijn', 'do', 'a','the','i', 'and', 'an', 'am', 'aan', 'de', 'to', "\'", "it", "in", 'at', 'for', 'of', 'en', 'on', 'is', 'with', 'we', 'are', 'if', 'you', 'op']     ## define stopwords
corpus =[token for token in tokens if token not in stops]
tokens = corpus 
text = nltk.Text(tokens)
fdist = nltk.FreqDist([w.lower() for w in text])

def typesOfUsers(fdist):
	languages = ['ruby', 'ios', 'c', 'javascript', 'html', 'android', 'python', 'rails', 'cocoa', 'php']
	designer  = ['ux', 'design', 'designer', 'creative', 'ui', 'social', 'media']
	business  = ['consultant', 'consultancy', 'founder', 'startup', 'startups', 'founder', 'co-founder', 'investor', 'entrepreneur', 'manager']
	other     = ['mobile', 'software', 'app', 'iphone', 'ipad', 'web', 'android', 'geek', 'amsterdam']
	for x in languages:
		print x + "," + str(fdist[x])
	for x in designer:
		print x + "," + str(fdist[x])
	for x in business:
		print x + "," + str(fdist[x])
	for x in other:
		print x + "," + str(fdist[x])

typesOfUsers(fdist)


def hashtagsToBigrams(hastags): # method not done!!! 
	# input of the file should be in this format: 
	   #amsterdamrs #iosdevcamp #mac
	   #amsterdam #appsterdam 
	   #iosdevcamp #amsterdam 
	#  ... etc 
	# output wil be a list of all bigrams and how often they occur 
	for row in hashtags: 
		print itertools.combinations(hastags,2)


## this bit is for printing out the most frequent words 
print "\n The most frequent words \n"
print fdist.keys()[:20]
print fdist.values()[:20]


## this bit is for printing out the most frequent bigrams 
print "\n The most frequent bigrams of words \n"
num_bigrams = 30
bigram_fd  = nltk.FreqDist(nltk.bigrams(tokens))
finder     = BigramCollocationFinder.from_words(tokens)
scored     = finder.score_ngrams(bigram_measures.raw_freq)
interestig_bigrams =  sorted(finder.nbest(trigram_measures.raw_freq, num_bigrams))
print sorted(finder.nbest(trigram_measures.raw_freq, num_bigrams))

## this bit will print out a string that can be copy pasted into csv 
f = open("graph_input.csv", "wb")
c = csv.writer(f, delimiter=",") ## this is the file that the csv will be written to 
for x in xrange(0,num_bigrams):
	new_line = str(bigram_fd.keys()[x]) + "," + str(bigram_fd.values()[x])
	new_line = new_line.translate(None, '.()\' ')
	c.writerow([new_line])
f.close()

## this bit will add a csv containing info about how often words are used
f = open("node_sizes.csv", "wb")
c = csv.writer(f, delimiter=",") ## this is the file that the csv will be written to 
token_freqd 	= nltk.FreqDist(tokens)
for x in xrange(0,200):
	new_line = str(token_freqd.keys()[x]) + "," + str(token_freqd.values()[x])
	new_line = new_line.translate(None, '.()\' ')
	c.writerow([new_line])
f.close()