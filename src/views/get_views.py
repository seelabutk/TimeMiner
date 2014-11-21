#!/usr/bin/env python

import gzip, glob, pickle, sys, os
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
		gz = os.popen('zcat ' + f).readlines()
		#gz = gzip.open(f).read().split('\n')
		found = []
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
					found.append(cols[1])
		for article in articles:
			if article not in found:
				result[article].append(0)
	result_name = str(year) + '-' + MONTH + '.txt'
	with open(result_name, 'wb') as out:
		for k in result.keys():
			out.write(k + '\n')
			for v in result[k]:
				out.write(str(v) + ' ')
			out.write('\n')

if __name__ == '__main__':
	articles = pickle.load(open('event_articles.pickle'))
	get_views(articles, YEAR)
