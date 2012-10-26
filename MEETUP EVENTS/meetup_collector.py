import time 
import datetime 
import json 
import csv 
import urllib 
import unicodedata
from numpy import *

def collectAllEvents(): 
	# purpose : collect all event data from appsterdam 
	#			the api only allows for 200 pages per call so we keep track of the 
	#			latest time value in the last api call. if the difference between 
	#			that time and the current time now is less than one week we stop 
	# input :  none 
	# output : csv file containing all the events with date, name and num rsvps 
	start_time 		= 0 
	week_seconds 	= 60*60*24*7*1000 
	current_time	= datetime.datetime.now() 
	current_time 	= int(time.mktime(current_time.timetuple())*1000)
	myfile 			= open('meetup_events.csv', 'wb')
	csv_writer		= csv.writer(myfile, quoting=csv.QUOTE_ALL)
	result 			= [] 
	while current_time - start_time > week_seconds:
		[start_time, main_dict] = doAPIcall(start_time) 
		for i in range(1,len(main_dict)): 
			event_id 		= main_dict[i]['id']
			event_name 		= main_dict[i]['name']
			current_date 	= main_dict[i]['time']
			num_people 		= main_dict[i]['yes_rsvp_count'] 
			event_name  	= unicodedata.normalize('NFKD', event_name).encode('ascii','ignore')
			csv_writer.writerow([str(event_id) + '|' + str(current_date) + '|' + str(event_name) + '|' + str(num_people)])
			result.append([str(event_id), str(current_date), str(event_name), str(num_people)])
	return result 

def doAPIcall(current_time): 
	# purpose : use the time value of last iteration to collect ALL meetup events 
	# input : current_time 	: int value that gets sent to meetup api 
	# output : dictionary containing new events 
	max_date = 6335954600000 
	website 	= 'https://api.meetup.com/2/events?key=3ad7a28717926121647c7618457a2&sign=true&time=' + str(current_time) + ',6335954600000&group_id=1853731&status=past&page=200'
	main_dict 	= json.loads(urllib.urlopen(website).read()).items()[1][1]
	latest_time = main_dict[len(main_dict)-2]['time']
	return [latest_time, main_dict]


def getEventData(event_id):
	# purpose 	: given an event_id we want to check how many people attended and at what date 
	# input 	: event_id			: string, ID that indicates the meetup event  
	# 			  event_name 		: string, name that indicates the meetup event 
	# output 	: a date utc number and an integer value for the number of people 
	website 	= 'https://api.meetup.com/2/event/' + event_id + '?key=3ad7a28717926121647c7618457a2&sign=true&page=20'
	event_data  = json.loads(urllib.urlopen(website).read(), 'latin-1').items()
	event_start = 0 
	new_people  = 0 
	for i in event_data: 
		if i[0] == 'time': 
			event_start	= i[1]
		if i[0] == 'yes_rsvp_count': 
			new_people 	= i[1]
	return [event_start, new_people]


## this bit is to attach people ... mwahahahahahah 

meetup_events			= collectAllEvents()
event_dict 				= {} 
for event in meetup_events:
	event_id 				= event[0]  
	website 				= 'https://api.meetup.com/rsvps?key=3ad7a28717926121647c7618457a2&sign=true&event_id=' + event_id + '&page=200'
	person_dict 			= json.loads(urllib.urlopen(website).read(), 'ISO-8859-1').items()[1][1]
	person_list 			= [] 
	for person in person_dict: 
		person_list.append( str(person['name'].encode('utf8', 'ignore')) )
	event_dict[str(event_id)] = person_list

all_people = [] 

for event_index in range(len(event_dict.keys())): 
	these_people 	= event_dict[event_dict.keys()[ event_index ]]
	new_people 	 	= list(set(list(these_people)).difference(set(all_people)))
	for person in new_people: 
		all_people.append(person)

## now comes the fun part ... each person gets a key which will be the matrix index 

translator_dict = {} 
for i in range(len(all_people)): 
	translator_dict[ all_people[i] ] = i 

first_row = all_people
myfile 			= open('meetup_people.csv', 'wb')
csv_writer		= csv.writer(myfile, quoting=csv.QUOTE_ALL)
csv_writer.writerow(all_people)
for event_index in range(len(event_dict.keys())):
	these_people 	= event_dict[event_dict.keys()[ event_index ]]
	new_row			= zeros(len(all_people))
	for person in these_people: 
		new_row[translator_dict[person]] = 1 
	first_row.append(new_row)
	csv_writer.writerow(new_row)


first_row = []
myfile 			= open('meetup_people_number_format.csv', 'wb')
csv_writer		= csv.writer(myfile, quoting=csv.QUOTE_ALL)
csv_writer.writerow(all_people)
for event_index in range(len(event_dict.keys())):
	these_people 	= event_dict[event_dict.keys()[ event_index ]]
	new_row			= zeros(len(all_people))
	for person in these_people: 
		new_row[translator_dict[person]] = 1 
		print str(translator_dict[person]) + ',' + str(event_index)
		csv_writer.writerow([translator_dict[person], event_index])
