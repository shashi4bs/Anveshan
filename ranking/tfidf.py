from text_normalizer import normalize_corpus
import math

def score(searchText, fetchedDocuments, allDocuments):
    '''
        searchResult -> searched query
        fetchedDocuments -> list of fetched results
        allDocuments -> all documents as set of keywords
    '''
    tokens = searchText.split()
    #tf(t, d) = count of t in document d / number of words in d
    tf = []
    idf = [] #document frequency
    fetchedDocuments = normalize_corpus(fetchedDocuments)
    for doc in fetchedDocuments:
        count = dict()
        for t in tokens:
            count[t] = 0
        for term in doc:
            if term in tokens:
                count[term] += 1
        countvalues = list(count.values())
        if len(doc)>0:
            idf.append([math.log(len(allDocuments)/(c+1)) for c in countvalues]) # append number of occurences in document
            for index, c in enumerate(countvalues):
                countvalues[index] /= len(doc)
        tf.append(countvalues) #append term frequency
    
    tfidfScore = []
    for x, y in zip(tf, idf):
        score = 0
        for i, j in zip(x, y):
            score += i * j
        tfidfScore.append(score)
    return tfidfScore
