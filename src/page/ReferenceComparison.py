import wikipedia
import re
import operator

def getCommonRefs(title1, title2):
    # retrieve pages
    page1 = wikipedia.page(title1)
    page2 = wikipedia.page(title2)

    # get lists of reference urls
    refs1 = page1.references
    refs2 = page2.references

    # find mutual references
    i = 0

    # print "mutual references:"
    commons = []
    for r in refs1:
        if r in refs2:
            commons.append(r)
            i = i + 1

    return commons

