#!/bin/bash

#da0.eecs.utk.edu

YEAR=2014

for MONTH in {05..08}; do
	URL="http://dumps.wikimedia.org/other/pagecounts-raw/$YEAR/$YEAR-$MONTH/"
	FILE="*.gz"
	DEST=/storage/da2_data/dahome/ahota/wiki/pagecount/$YEAR-$MONTH/
	mkdir $DEST
	wget --no-parent -r -nd -A $FILE -P $DEST $URL
done
