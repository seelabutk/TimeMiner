import re
import sys
import pprint
import wikipedia
import pickle

# Extracts inlinks, outlinks, backlinks and their titles from a Wikipedia pagelinks file and page file
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
        id_start = self.page_info.find('(' + str(id) + ',')
        title_start = self.page_info.find('\'', id_start) + 1
        title_end = self.page_info.find('\',', title_start)
        return self.page_info[title_start:title_end]

    def getId(self, title):
        print 'Looking for the ID of ' + title
        result = self.page_info.find('\'' + title + '\',')
        if result == -1:
            return -1
        id_start = self.page_info.rfind('(', result - 100, result) + 1
        id_end = self.page_info.find(',', id_start, result)
        id = self.page_info[id_start:id_end]
        print self.page_info[id_start-1:id_end+1] 
        return int(id)
        
    def getInLinks(self, title):
        count = 0
        inlinks = set()
        results = re.finditer('\'' + title + '\'', self.contents)
        for result in results:
            id_start = self.contents.rfind('(', result.start() - 100, result.start()) + 1
            id_end = self.contents.find(',', id_start, result.start())
            id = self.contents[id_start:id_end]
            #title = self.getTitle(id, False)
            inlinks.add(int(id))
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
            id = self.getId(title)
            outlinks.add(id)

        return outlinks
    
# Extracts backlinks by intersecting inlinks and outlinks
def extractBackLinks(events):
    for event in events:
        inlinks = set(pickle.load(open(event + '_inlink_ids.pickle')))
        outlinks = set(pickle.load(open(event + '_outlink_ids.pickle')))
        backlinks = inlinks.intersection(outlinks)
        pickle.dump(backlinks, open(event + '_backlink_ids.pickle', 'w'))
        pprint.pprint(backlinks)
        print len(backlinks)

def extractInLinkIds(wikiex, titles, nicknames):
    for i in range(len(titles)):
        inlinks = wikiex.getInLinks(titles[i])
        pickle.dump(inlinks, open(nicknames[i] + '_inlink_ids.pickle', 'w'))
        pprint.pprint(inlinks)

# Extracts the titles of backlinked articles that are saved in the backlinks file
def extractTitles(wikiex, nicknames):
    counter = 0
    for i in range(len(nicknames)):
        link_ids = pickle.load(open(nicknames[i] + '_backlink_ids.pickle'))
        titles = []
        for id in link_ids:
            titles.append(wikiex.getTitle(id))
            sys.stdout.write('%d\r'%counter)
            sys.stdout.flush()
            counter += 1

        pickle.dump(titles, open(nicknames[i] + '_backlink_titles.pickle', 'w'))
        pprint.pprint(titles)

def extractOutLinkIds(wikiex, titles, nicknames):
    for i in range(len(titles)):
        outlinks = wikiex.getOutLinks(titles[i])
        pickle.dump(outlinks, open(nicknames[i] + '_outlink_ids.pickle', 'w'))
        pprint.pprint(outlinks)

if __name__=='__main__':
    nicknames = ['ebola', 'mh370', 'olympics']
    titles = ['Ebola_virus_disease', 'Malaysia_Airlines_Flight_370', '2014_Winter_Olympics']
    wikiex = WikiLinksExtractor()
    wikiex.init()
    # extractInLinkIds(wikiex, titles, nicknames);
    # extractOutLinkIds(wikiex, titles, nicknames)
    # extractBackLinks(nicknames)
    extractTitles(wikiex, nicknames)
