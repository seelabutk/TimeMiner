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

	def getTitle(self, id, fromDB=True):
		if not fromDB:
			try:
				p = wikipedia.page(pageid=id)
				return p.title
			except:
				return ''
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

def extractInLinkIds():
	links = WikiLinksExtractor()
	links.init()
	inlinks = links.getInLinks('2014_Winter_Olympics')
	pickle.dump(inlinks, open('olympics_inlink_ids.pickle', 'w'))
	pprint.pprint(inlinks)

if __name__=='__main__':
	extractInLinkIds();
