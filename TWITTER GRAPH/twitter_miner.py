## appsterdam twitter data 

## usage:   we open a csv file with names of companies or phenomenon that are 
##          of interest to the amsterdam tech community. these subjects are 
##          searched on twitter. the tweets will give us a new list of users and
##          hashtags. these will be searched again and through a breadth first 
##          search we will come to an even larger graph. this graph is then stored
##          with a date. this script needs to be rerun such that the graph is updated 
##          we also keep the messages in the tweets

## example calls: 
##        $ python mega_twitter_parser.py 

## prerequisites: 
##      python 2.7.3 
##      nltk package 
##      numpy

## output : a csv file containing all the connections between users/hashtages 
##          a csv file containing the actual tweets 

import os, sys; sys.path.insert(0, os.path.join("..", ".."))
from pattern.web import Twitter, hashtags
from pattern.db  import Datasheet, pprint
import numpy as np
from nltk.corpus import stopwords
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
import unicodedata
import time
from datetime import date 

twitter_subjects      = np.genfromtxt('twitter_subjects.csv', skip_header=False, delimiter=',', dtype='|S')

try: 
    # We store tweets in a Datasheet that can be saved as a text file (comma-separated).
    # In the first column, we'll store a unique ID for each tweet.
    # We only want to add the latest tweets, i.e., those we haven't previously encountered.
    # With an index on the first column we can quickly check if an ID already exists.
    # The index becomes important once more and more rows are added to the table (speed).
    table = Datasheet.load("current_tweets.csv")
    index = dict.fromkeys(table.columns[0], True)
except:
    table = Datasheet()
    index = {}

engine = Twitter(language="en")
tweet_csv = []
table = [] 
for twitter_subject in twitter_subjects:
    # With cached=False, a live request is sent to Twitter,
    # so we get the latest results for the query instead of those in the local cache.
    for tweet in engine.search(twitter_subject, count=275, cached=False):
        # Create a unique ID based on the tweet content and author.
        new_line = '@'+tweet.author + ' , ' + tweet.description + ' , ' + str(tweet.values()[5]) + ' , ' + str(tweet.url)
        id = hash(tweet.author + tweet.description)
        # Only add the tweet to the table if it doesn't already contain this ID.
        if len(table) == 0 or id not in index:
            tweet_csv.append(new_line)
            norm_descr  = unicodedata.normalize('NFKD', tweet.description).encode('ascii','ignore')
            norm_author = unicodedata.normalize('NFKD', tweet.author).encode('ascii','ignore')
            table = table + ['@'+ str(norm_author) + ' ' + str(norm_descr)]
            index[id] = True

## this bit will save all the tweets with the date into a csv file with a date attached in the file name 
str_today = 'tweets' + str(date.today().day) + '-' + str(date.today().month) + '-' + str(date.today().year) + '.csv'
f = open(str_today, "wb")
c = csv.writer(f, delimiter=",") ## this is the file that the csv will be written to 
for x in xrange(0,len(tweet_csv)):
    new_line = tweet_csv[x][0] + '' + tweet_csv[x][1] + '' + tweet_csv[x][2]
    new_line = unicodedata.normalize('NFKD', new_line).encode('ascii','ignore')
    new_line = str(new_line).translate(None, '.()\' ')
    c.writerow([new_line])
f.close()

bigram_table = Datasheet()
all_tokens   = []

for row in table: 
    tweet = str(row).lower()
    tokens = []
    for i in range(0,len(word_tokenize(tweet))): 
        if word_tokenize(tweet)[i] == '@':
            tokens.append( str('@' + word_tokenize(tweet)[i+1]) )
        if word_tokenize(tweet)[i] == '#':
            tokens.append( str('#' + word_tokenize(tweet)[i+1]) ) 
    new_bigrams = nltk.bigrams(tokens)
    for bigram in new_bigrams: 
        bigram_table.append(bigram)
    for token in tokens:
        all_tokens.extend(tokens)

token_freq = nltk.FreqDist(all_tokens)

str_today = 'tweet_graph_' + str(date.today().day) + '-' + str(date.today().month) + '-' + str(date.today().year) + '.csv'
bigram_table.save(str_today)

new_twitter_subjects = list(set(all_tokens))
another_table = Datasheet()

# save the original list of twitter users, we'll use this in cytoscape 
spamWriter = csv.writer(open('original_twitter.csv', 'wb'), delimiter=' ', quotechar='|')
for i in list(set(all_tokens)): 
    spamWriter.writerow([i, 1])

for twitter_subject in new_twitter_subjects:
    # With cached=False, a live request is sent to Twitter,
    # so we get the latest results for the query instead of those in the local cache.
    for tweet in engine.search(twitter_subject, count=275, cached=False):
        # Create a unique ID based on the tweet content and author.
        id = hash(tweet.author + tweet.description)
        # Only add the tweet to the another_table if it doesn't already contain this ID.
        if len(another_table) == 0 or id not in index:
            another_table.append([' @'+tweet.author + ' ' + tweet.description])
            index[id] = True

another_table.save("even_moretweets.txt", delimiter=" ")

print "Total results:", len(another_table)     

big_bigram_table = Datasheet()
big_all_tokens   = []

for row in another_table: 
    tweet = str(row).lower()
    tokens = []
    for i in range(0,len(word_tokenize(tweet))): 
        if word_tokenize(tweet)[i] == '@':
            tokens.append( str('@' + word_tokenize(tweet)[i+1]) )
        if word_tokenize(tweet)[i] == '#':
            tokens.append( str('#' + word_tokenize(tweet)[i+1]) ) 
    new_bigrams = nltk.bigrams(tokens)
    for bigram in new_bigrams: 
        big_bigram_table.append(bigram)
    for token in tokens:
        big_all_tokens.extend(tokens)

token_freq = nltk.FreqDist(big_all_tokens)

str_today = 'tweet_graph_' + str(date.today().day) + '-' + str(date.today().month) + '-' + str(date.today().year) + '.csv'
big_bigram_table.save("biggest_tweet_graph2.csv")