import re
import sys
import pprint
import wikipedia
import pickle

class WikiLinksExtractor:
	insert_pattern=r"""\([0-9]*,0,(\\[\'\"])(?:\\\\\1|.)*?\1,[0-9]*\)"""
	pagelinks_filename = 'enwiki-20141008-pagelinks.sql'
	page_filename = 'enwiki-20141008-page.sql'
	def __init__(self):
		pass

	def init(self):
		print 'Object initialized'
		self.f = open(self.pagelinks_filename)
		self.contents = self.f.read()
		self.f.close()
		print 'Finished reading the pagelink file into memory'
		page_file = open(self.page_filename)
		self.page_info = page_file.read()
		page_file.close()
		print 'Finished reading the page info file into memory'

	def getTitle(self, id):
		try:
			p = wikipedia.page(pageid=id)
			return p.title
		except:
			id_start = self.page_info.find('(' + str(id))
			title_start = self.page_info.find('\'', id_start) + 1
			title_end = self.page_info.find('\',', title_start)
			return self.page_info[title_start:title_end]
		
	def getInLinks(self, title):
		count = 0
		inlinks = set()
		results = re.finditer(title + '\'', self.contents)
		for result in results:
			id_start = self.contents.rfind('(', result.start() - 100, result.start()) + 1
			id_end = self.contents.find(',', id_start, result.start())
			id = self.contents[id_start:id_end]
			#title = self.getTitle(id, False)
			inlinks.add(id)
			#print title
			count += 1
		print 'Found ' + str(count) + ' links.'
		return inlinks

	def getOutLinks(self, title):
		main_article = wikipedia.page(title)
		outlinks = set()
		results = re.finditer('\(' + str(main_article.pageid) + ',', self.contents)
		for result in results:
			title_start = self.contents.find('\'', result.start()) + 1
			title_end = self.contents.find('\',', title_start)
			title = self.contents[title_start:title_end]
			outlinks.add(title)

		return outlinks
	

def extractBackLinks(events):
	for event in events:
		inlinks = set(pickle.load(open(event + '_inlink_titles.pickle')))
		outlinks = set(pickle.load(open(event + '_outlink_titles.pickle')))
		backlinks = inlinks.intersection(outlinks)
		pickle.dump(backlinks, open(event + '_backlinks_titles.pickle', 'w'))
		pprint.pprint(backlinks)
		print len(backlinks)

def extractInLinkIds():
	links = WikiLinksExtractor()
	links.init()
	inlinks = links.getInLinks('2014_Winter_Olympics')
	pickle.dump(inlinks, open('olympics_inlink_ids.pickle', 'w'))
	pprint.pprint(inlinks)

def extractTitles():
	link_ids = pickle.load(open('olympics_inlink_ids.pickle'))
	titles = []
	wikilinks = WikiLinksExtractor()
	wikilinks.init()
	for id in link_ids:
		titles.append(wikilinks.getTitle(id))
	pickle.dump(titles, open('olympics_inlink_titles.pickle', 'w'))
	pprint.pprint(titles)

def extractOutLinkTitles(title, event):
	extractor = WikiLinksExtractor()
	extractor.init()
	outlinks = extractor.getOutLinks(title)
	pickle.dump(outlinks, open(event + '_outlink_titles.pickle', 'w'))
	pprint.pprint(outlinks)

if __name__=='__main__':
	# extractInLinkIds();
	# extractTitles()
	extractOutLinkTitles('Malaysia_Airlines_Flight_370', 'mh370')
	extractOutLinkTitles('2014_Winter_Olympics', 'olympics')
	extractBackLinks(['ebola', 'mh370', 'olympics'])
