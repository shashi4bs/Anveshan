import sys
import os
sys.path.append(os.path.abspath('../Anvesion'))

from text_normalizer import normalize_corpus
from db import resultsCollection as r
import numpy as np

results = r.find()
word_dictionary = dict()
tokenized_text = []
raw_text = []

class Index:
    def __init__(self):
        self.name = None
        self.nextIndexes = []
        self.documents = []

    def __str_(self):
        return "name: {}, next: {}, documents: {}".format(self.name, [s.name for s in self.nextIndexes], self.documents)

def sortByFrequency(e):
    return word_dictionary[e]
#sort tokenized_text by frequency(keys)


def iterateIndex(index, text, num):
    if index.name != text[0]:
        return False
    if len(text)>1:
        iterated = []
        for n in index.nextIndexes:
            iterated.append(iterateIndex(n, text[1:], num))
        #print(iterated, any(iterated))
        if not any(iterated):
            index.nextIndexes.append(createIndex(index, text[1:], num))
    return True

def createIndex(parentIndex, text, num):
    index = Index()
    index.name = text[0]
    if len(text)>1:
        index.nextIndexes.append(createIndex(index, text[1:], num))
    else:
        index.documents = raw_text[num-1]
        #print(sorted(tokenized_text[num-1], key=sortByFrequency, reverse=True))
        #print(index)
    return index


headIndex = Index()
headIndex.name = 'HeadIndex'
num = 0

print("Creating Index")

for res in results:
    text = []
    text.extend(np.array(normalize_corpus(res["text"])).ravel().tolist())
    text.extend(np.array(normalize_corpus(res["author"])).ravel().tolist())
    text.extend(np.array(normalize_corpus(res["tags"])).ravel().tolist())
    #handling type(text) == list
    to_remove = []
    for t in text:
        if type(t) is list:
            text.extend(t)
            to_remove.append(t)
    for t in to_remove:
        text.remove(t)

    for t in text:            
        if t not in word_dictionary.keys():
            word_dictionary[t] = 1
        else: 
            word_dictionary[t] += 1
    text = list(set(text))
    tokenized_text.append(text)
    raw_text.append(res["text"][0])

for t in tokenized_text:
    sorted_t = sorted(t, key=sortByFrequency, reverse=True)
    if len(headIndex.nextIndexes) is 0:
        headIndex.nextIndexes.append(createIndex(headIndex, sorted_t, num))
        num += 1
    else:
        num += 1
        inheadIndex = [iterateIndex(n, sorted_t, num) for n in headIndex.nextIndexes]
        if not any(inheadIndex):
            headIndex.nextIndexes.append(createIndex(headIndex, sorted_t, num))

print("Done Indexing")

documents = []

def extractDocument(index):
    global documents
    if len(index.documents)>0:
        documents.append(index.documents)
    for n in index.nextIndexes:
        extractDocument(n)
    

def searchIndexedContent(index, token):
    if index.name == token:
        extractDocument(index)
    else:
        for n in index.nextIndexes:
            searchIndexedContent(n, token)

def searchToken(token):
    global documents
    documents = []
    for n in headIndex.nextIndexes:
        searchIndexedContent(n, token)
    return documents

print(searchToken("die"))
