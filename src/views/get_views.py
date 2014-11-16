#!/usr/bin/env python

import gzip, glob, pickle
from collections import defaultdict

FILE_PATH = '/export/data/dahome/ahota/wiki/pagecount/{YYYY}-{MM}/*.en.gz'
YEAR = 2014

def get_views(articles, year):
	
	result = defaultdict(int)
	month_strs = [ str(i).zfill(2) for i in range(1, 13) ]
	for month in month_strs:
		fname = FILE_PATH.format( YYYY=str(year), MM=month )
		files = glob.glob(fname)
		for f in files:
			try:
				gz = gzip.open(f).read().split('\n')
				for line in gz:
					cols = line.split()
					if cols[1] in articles:
						result[ cols[1] ] += cols[2]
						print cols[1] + ' added ' + cols[2]
	pickle.dump(results, open('results.p', 'wb'))

if __name__ == '__main__':
	a = ['Ebola_virus_disease']
	get_views(a, YEAR)
