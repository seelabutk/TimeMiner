#!/usr/bin/env python

import wikipedia, glob
from collections import defaultdict

def special(article):
	return article.startswith('Special:') or article.startswith('File:') or article == 'Main_Page' or article == 'en'

LOG_DIR = '/export/data/dahome/ahota/wiki/pagecount/2014-03/'
FN_GLOB = 'pagecounts-20140308-*.search'

results = defaultdict(int)
files = glob.glob(LOG_DIR+FN_GLOB)

for filename in files:
	print 'Parsing ' + filename + '...'
	with open(filename) as f:
		lines = f.readlines()
		for line in lines:
			items = line.split()
			if not special(items[1]):
				results[items[1]] += int(items[2])

print 'Sorting...'
page_hits = sorted(results.iteritems(), key=lambda (k, v): v, reverse=True)
print 'Sorted.'
print 'Top hit:', page_hits[0][0], page_hits[0][1]
print 'Writing...'
with open('en_search.log', 'wb') as log:
	for i in range(100):
		log.write(str(i) + page_hits[i][0] + '\t' + str(page_hits[i][1]) + '\n')

print 'Done'
