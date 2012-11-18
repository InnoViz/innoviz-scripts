#####
# One line summary.
#	This script adds lat lng information to a csv file containing company names.	
# 
# Usage:
#  	python add_companies.py -> member_companies.csv 
# 		in the /data folder you need an original member_companies.csv file containing member_id - company links 
##### 

from HTMLParser import HTMLParser
import numpy as np
API_KEY = 'AIzaSyB_jdO5TBgBDwjOjHatA16CgSjVzjCcLa4'
from googlemaps import GoogleMaps 
import pandas 
from bs4 import BeautifulSoup
gmaps = GoogleMaps(API_KEY)



class MLStripper(HTMLParser):
	# we use this to strip html tags 
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def zoekBedrijf(zoekterm):
	# search the kvk website for a company and then parse the address from it 
	website 	='http://www.kvk.nl/uitgebreid-zoeken/?handelsnaam=' + zoekterm + '&kvknummer=&straat=&huisnummer=&postcode=&plaats=&hoofdvestiging=1&rechtspersoon=1&nevenvestiging=1' 
	html	 	= urllib.urlopen(website).read()
	soup 		= BeautifulSoup(html)
	if soup.body.find_all('li')[0].ul == None:
		return 'none' 
	adres 		= str(soup.body.find_all('li')[0].ul.li.nextSibling.nextSibling.nextSibling.nextSibling)
	adres		= adres[4:][:len(adres)-9]
	plaats 		= str(soup.body.find_all('li')[0].ul.li.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling)
	plaats 		= plaats[4:][:len(adres)-5]
	return adres + ' ' + plaats + ' , Netherlands'

member_companies 		= np.genfromtxt('input_data/link.csv', skip_header=False, delimiter=',', dtype='|S')
data 					= pandas.read_csv('input_data/link.csv', delimiter=',')
person_list 			= [['bart', 'gillz'], ['vincent','localsensor']]

	for person in member_companies: 
		output_person = list(person)
		if person[1] != 'none': 
			company_address 		= strip_tags(zoekBedrijf(person[1]))
			if company_address != 'none': 
				try: 
					lat, lng 				= gmaps.address_to_latlng(company_address)
					output_person.append(lat) 
					output_person.append(lng)
				except: 
					pass 
		print output_person


try:
    do_something()
except Exception:
    pass


