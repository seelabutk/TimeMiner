#!/usr/bin/env python

import requests, json, pickle, os

PREFIX = 'http://stats.grok.se/json/en/'

def get_views(title, year):
    if os.path.isfile(title+str(year)+'.p'):
        print 'Already have dump for', title
        return
    result = {}
    for month in range(13):
        url = PREFIX + str(year) + str(month).zfill(2) + '/' + title
        tmp = requests.get(url).json()['daily_views']
        result.update(tmp)
    print 'Retrieved ' + str(len(result.keys())) + ' days of page view data for article ' + title
    pickle.dump(result, open(article+str(year)+'.p', 'wb'))
    print 'Dumped to pickle file'
    return result

year = 2014
articles = ['Malaysia_Airlines_Flight_370', '2014_Winter_Olympics', 'Ebola_virus_disease']
for article in articles:
    get_views(article, year)

