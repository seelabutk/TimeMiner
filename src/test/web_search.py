#!/usr/bin/env python

import wikipedia
from collections import defaultdict

def word_count(items):
	results = defaultdict(int)
	for item in items:
		tokens = item.split()
		for t in tokens:
			results[t] += 1
	sorted_results = sorted(results.iteritems(), key=lambda (k, v): v, reverse=True)
	return sorted_results

with open('en_search.log') as f:
	top = f.readline().strip()

print 'First line = ' + top
print 'Top article name = ' + top.split()[2]

top_name = top.split()[2]
top_article = wikipedia.page(top_name)
top_article_links = top_article.links

wc_links = word_count(top_article_links)[:5]

print 'Top 5 words in links for ' + top_name + ':'
for link in wc_links:
	print link[0] + '\t' + str(link[1])

print 'Finding linkbacks...'
link_back = []
#Just realized:
#wc_links is a list of words, not link titles
#Even if we have link titles, we don't have the target of the link
#It seems like the only way to get the target is to call the HTML function and
#parse it for the link title, which would lead to the link target
