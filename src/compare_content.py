import wikipedia
import re
import operator

# test titles
title1 = "Eboal_virus_disease"
title2 = "Ebolavirus"

# retrieve pages
page1 = wikipedia.page(title1)
page2 = wikipedia.page(title2)

# split words
words1 = iter(re.split('\s', page1.content))
words2 = iter(re.split('\s', page2.content))

# store in dictionaries
dic1 = {}
for w in words1:
	if w in dic1:
		dic1 [w] = dic1 [w] + 1
	else:
		dic1[w] = 1

dic2 = {}
for w in words2:
	if w in dic2:
		dic2 [w] = dic2 [w] + 1
	else:
		dic2[w] = 1

# from here we need to determine how figure the weighting

# this approach finds how many mutual words there are in the top 10 most common words on each page

# List of unhelpful strings
stop_words = ["a", "A", "an", "An", "the", "The", "of", "in", "to", "for", "with", "on", "at", "from", "by", "about", "as", "into", "like", "through", "after", "over", "between", "out", "against", "during", "without", "before", "under", "around", "among", "is", "was", "were", "will", "be", "has", "been", "are", "or", "and", "but", "however", "therefore", "that", "===", "=="]

for w in stop_words:
	dic1.pop(w, None)
	dic2.pop(w, None)

# sort to access top 10
dic1_sorted = sorted (dic1.iteritems(), key = operator.itemgetter(1), reverse = True)
dic2_sorted = sorted (dic2.iteritems(), key = operator.itemgetter(1), reverse = True)

# print for now
dic1_top = min(len(dic1_sorted), 10)
for i in range(1, dic1_top, 1):
	print dic1_sorted[i][0]+"\t"+str(dic1_sorted[i][1])

print "\n\n"

dic2_top = min(len(dic2_sorted), 10)
for i in range(1, dic2_top, 1):
	print dic2_sorted[i][0]+"\t"+str(dic2_sorted[i][1])

