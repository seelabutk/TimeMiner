#!/bin/bash

#da2.eecs.utk.edu

YEAR=2014

for MONTH in {01..04}; do
	URL="http://dumps.wikimedia.org/other/pagecounts-raw/$YEAR/$YEAR-$MONTH/"
	FILE="*.gz"
	DEST=/export/data/dahome/ahota/wiki/pagecount/$YEAR-$MONTH/
	mkdir $DEST
	wget --no-parent -r -nd -A $FILE -P $DEST $URL
done
