import urllib2
import sys, os
from HTMLParser import HTMLParser
import json
import json
import urllib2


limit = 500
wikis = {}

def count_backlink(page):
    org_url = "https://en.wikipedia.org//w/api.php?action=query&list=backlinks&format=json&bltitle=%s&blfilterredir=all&bllimit=%s&continue="
   
    tofetch = 1
    url = org_url
    back_links = 0
    tofetch = 1
    unicode_page = page.encode('utf-8')
    full_url = org_url %(unicode_page, limit)
    url = full_url 
    while tofetch:
        data = urllib2.urlopen(url).read()
        json_data = json.loads(data)
        try:
            #print json_data['continue']
            url = full_url + "&blcontinue=%s" %(json_data['continue']['blcontinue'])
            #print url
            back_links += limit
        except:
            for key in json_data['query']['backlinks']:
                back_links += 1
            tofetch = 0
    return back_links
#
def get_wiki_pages(page):
   
    org_url = "https://en.wikipedia.org/w/api.php?action=query&prop=links&format=json&titles=%s&pllimit=%s" %(page, limit)
    tofetch = 1
    page_url = {}
    back_links = 0
    url = org_url
    
    while tofetch:
        data = urllib2.urlopen(url).read()
        json_data = json.loads(data)
        for i in json_data['query']['pages']:
            for link in json_data['query']['pages'][i]['links']:
                 title = link['title'].replace(" ", "_")
                 page_url[title] = 0
        try:
            #print json_data['continue']
            url = org_url + "&plcontinue=%s" %(json_data['continue']['plcontinue'])
            print url
            back_links += limit
        except:
            tofetch = 0
    #print json_data
    #print page_url
    return page_url

response = urllib2.urlopen('https://en.wikipedia.org/wiki/Rail_lengths')
html = response.read()

#parser = MyHTMLParser()
#parser.feed(html)
most_popular_count = 0
most_popular_page = ""
wikis =  get_wiki_pages("Fishplate")
for i in wikis:
    if i == "Main_Page":
        print "skip"
        continue
    if i.find(":") >= 0:
        continue
    try:
        popularity = count_backlink(i)
    except: # retry
        popularity = count_backlink(i)
    wikis[i] = popularity
    print i, popularity
    if popularity > most_popular_count:
        most_popular_count = popularity
        most_popular_page = i
print "*********"
print most_popular_page, most_popular_count
print "*********"

