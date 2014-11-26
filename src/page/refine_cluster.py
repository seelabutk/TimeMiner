#!/usr/bin/env python

import ContentComparison, ReferenceComparison
import pickle, wikipedia, pprint
from collections import Counter

def cull(seed, articles):
    try:
        common_ref_pages = pickle.load(open(seed+'_crp.pickle'))
    except:
        seed_page = wikipedia.page(seed)
        common_ref_pages = [a for a in articles if ReferenceComparison.getCommonRefs(seed_page, a) > 0]
        pickle.dump(common_ref_pages, open(seed+'_crp.pickle', 'wb'))
        #print str(len(common_ref_pages)) + ' articles with common references to ' + seed + ':'
        #pprint.pprint(common_ref_pages)
    return common_ref_pages

def further_cull(seed, articles):
    results = []
    words = []
    for a in articles:
        common_words = ContentComparison.compareWordCount(seed, a)
        if(len(common_words) > 2):
            #print 'Common words between ' + seed + ' and ' + a
            #pprint.pprint(common_words)
            results.append(a)
            words += common_words
    return results, words

if __name__ == '__main__':
    clusters = {'Ebola_virus_disease' : pickle.load(open('../links/ebola_backlink_titles.pickle')),
                'Malaysia_Airlines_Flight_370' : pickle.load(open('../links/mh370_backlink_titles.pickle')),
                '2014_Winter_Olympics' : pickle.load(open('../links/olympics_backlink_titles.pickle'))
        }
    for seed in clusters:
        common_ref_pages = cull(seed, clusters[seed])
        final_cluster, event_words = further_cull(seed, common_ref_pages)
        event_word_counter = Counter(event_words)
        event_word_sorted = event_word_counter.most_common(4)
        print 'Event words for ' + seed + ':'
        pprint.pprint([word[0] for word in event_word_sorted])
        print seed + ' final_cluster length = ' + str(len(final_cluster))

