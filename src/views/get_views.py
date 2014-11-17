#!/usr/bin/env python

import gzip, glob, pickle, sys
from collections import defaultdict

FILE_PATH = '/export/data/dahome/ahota/wiki/pagecount/{YYYY}-{MM}/*.en.gz'
MONTH = sys.argv[1].zfill(2)
YEAR = 2014

def get_views(articles, year):
	
	result = defaultdict(list)
	fname = FILE_PATH.format( YYYY=str(year), MM=MONTH )
	files = glob.glob(fname)
	for f in files:
		print_name = f[f.rfind('/') + 12:len(f) - 6]
		gz = gzip.open(f).read().split('\n')
		if len(gz) < 5:
			for a in articles:
				result[a].append(0)
			continue
		for line in gz:
			cols = line.split()
			if len(cols) == 4:
				if cols[1] in articles:
					result[ cols[1] ].append(cols[2])
					print print_name + ': ' + cols[1] + ' added ' + cols[2]
				else:
					result[ cols[1] ].append(0)
	result_name = str(year) + '-' + MONTH + '.p'
	pickle.dump(results, open(result_name, 'wb'))

if __name__ == '__main__':
	articles = pickle.load(open('event_articles.pickle'))
	get_views(articles, YEAR)
