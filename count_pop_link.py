import urllib2
import sys, os, signal
import json
import json
import urllib2


limit = 500
wikis = {}

# Count number of backlinks using wiki API of a page
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

# Find all pages within that page
def get_wiki_pages(page):
   
    unicode_page = page.encode('utf-8')
    org_url = "https://en.wikipedia.org/w/api.php?action=query&prop=links&format=json&titles=%s&pllimit=%s" %(unicode_page, limit)
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
            url = org_url + "&plcontinue=%s" %(json_data['continue']['plcontinue'])
            back_links += limit
        except:
            tofetch = 0
    return page_url

def verify_url(url):
    # need to use proper validator
    if (url.find("wikipedia.org/wiki/") >= 0):
        return True
    return False

def sigint_handler(signal, frame):
    print "Keyboard Interrupt pressed"
    sys.exit(0)

if __name__ == "__main__":
    most_popular_count = 0
    most_popular_page = ""
    popularity = 0
    count = 0
    if len(sys.argv) != 2:
        print "Usages  %s wiki url" %(sys.argv[0])
        sys.exit(-1)

    signal.signal(signal.SIGINT, sigint_handler)
    if verify_url(sys.argv[1]):
        try:
            url = sys.argv[1]
            page_name = url.split("/")[len(url.split("/")) - 1] 
            print page_name
            wikis =  get_wiki_pages(page_name)
        except:
            print "Please provide proper wiki url"
            sys.exit(-1)

    else:
        print "Please provide proper wiki url"
        sys.exit(-1)
    for i in wikis:
        if i == "Main_Page":
            print "skip"
            continue
        if i.find(":") >= 0:
            continue
        #retry
        for k in range(0, 5):
            try:
                popularity = count_backlink(i)
                break
            except Exception, e:
                continue
        wikis[i] = popularity
        if popularity > most_popular_count:
            most_popular_count = popularity
            most_popular_page = i
        count += 1
        print "Complted %d/%d, current popular %s:%d(backlink)" %(count, len(wikis), str(most_popular_page), most_popular_count)
    
    print "Most popular link: %s with count %d" %(most_popular_page, most_popular_count)

