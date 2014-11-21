import wikipedia
import re
import operator

# test titles
title1 = "Eboal_virus_disease"
title2 = "Ebolavirus"

# retrieve pages
page1 = wikipedia.page(title1)
page2 = wikipedia.page(title2)

# get lists of reference urls
refs1 = page1.references
refs2 = page2.references

# find mutual references
i = 0

print "mutual references:"
for r in refs1:
	if r in refs2:
		print r
		i = i + 1

print "\nnumber of mutual references:", i
