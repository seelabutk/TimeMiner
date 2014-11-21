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
