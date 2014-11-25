import wikipedia
import re
import operator
from collections import Counter
from nltk.corpus import stopwords
import pprint

def getWordCount(titles):
    for title in titles:
        try:
            words = iter(re.split('\s', wikipedia.page(title).content))
            stops = stopwords.words('english')
            stops += ['==', '===']
            counter = Counter([word.lower() for word in words if word not in stops])
        except:
            pass

    return counter

def compareWordCount(title1, title2):
    stops = stopwords.words('english') + [u'==', u'===', u'']
    seed_counter = Counter([word for word in iter(re.split('\s', wikipedia.page(title1).content.lower()))
        if word not in stops]).most_common(10)
    comp_counter = Counter([word for word in iter(re.split('\s', wikipedia.page(title2).content.lower()))
        if word not in stops]).most_common(10)
    results = []
    for wordcount in seed_counter:
        word = wordcount[0]
        for wordcount2 in comp_counter:
            if wordcount2[0] == word:
                results.append(word)
    return results
