import wikipedia
import re
import operator


# Changed input to page1 and title2 so that we don't constantly retrive the
# same page when called from refine_cluster.py
def getCommonRefs(page1, title2):

    try:
        # retrieve pages
        #page1 = wikipedia.page(title1)
        page2 = wikipedia.page(title2)

        # get lists of reference urls
        refs1 = page1.references
        refs2 = page2.references
    except:
        return 0

    # find mutual references
    i = 0

    # print "mutual references:"
    commons = [r for r in refs1 if r in refs2]
    i = len(commons)
    '''
    commons = []
    for r in refs1:
        if r in refs2:
            commons.append(r)
            i = i + 1
    '''
    return i

