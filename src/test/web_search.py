#!/usr/bin/env python

import wikipedia
from collections import defaultdict
from bs4 import BeautifulSoup

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
print 'Getting HTML...'
top_article_soup = BeautifulSoup(top_article.html())
print 'Extracting links...'
top_article_soup_links = []
for link in top_article_soup.find_all('a'):
    try:
        top_article_soup_links.append(link.contents[0])
    except:
        pass

top_article_wiki_links = top_article.links

print 'Found ' + str(len(top_article_links)) + ' links'
#top_article_links = top_article.links

print 'Counting words in links...'
wc_links = word_count(top_article_links)[:5]

print 'Top 5 words in links for ' + top_name + ':'
for link in wc_links:
	print link[0] + '\t' + str(link[1])

important_links = set([link for link in top_article_links for wc in wc_links if wc[0] in link])
print str(len(important_links)) + ' links contain a top 5 word'

print 'Finding linkbacks...'
link_back = []
#Just realized:
#wc_links is a list of words, not link titles
#Even if we have link titles, we don't have the target of the link
#It seems like the only way to get the target is to call the HTML function and
#parse it for the link title, which would lead to the link target
