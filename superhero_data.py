import urllib2
import json
import pprint
import re
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup

class myhtmlparser(HTMLParser):
    def __init__(self):
        self.reset()
        self.NEWTAGS = []
        self.NEWATTRS = []
        self.HTMLDATA = []
    def handle_starttag(self, tag, attrs):
        self.NEWTAGS.append(tag)
        self.NEWATTRS.append(attrs)
    def handle_data(self, data):
        self.HTMLDATA.append(data)
    def clean(self):
        self.NEWTAGS = []
        self.NEWATTRS = []
        self.HTMLDATA = []

parser = myhtmlparser()
superheroFactDict = {}

response = urllib2.urlopen('http://marvel.wikia.com/api/v1/Articles/Top/?limit=100&category=Characters')
#response = urllib2.urlopen('http://google.com')
tmp = json.load(response)
with open('superhero_db/superhero_list.json', 'wb') as outfile:
    json.dump(tmp, outfile)

pprint.pprint(tmp)
basepath = tmp['basepath']
for entry in tmp['items']:
    name = entry['title'].replace('(Earth-616)', '').strip()
    url = basepath + entry['url']
    hero_page = urllib2.urlopen(url).read()
    with open('superhero_db/' + name + '.html', 'wb') as outfile:
        outfile.write(hero_page)
