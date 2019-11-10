import sys
import os
sys.path.append(os.path.abspath('../Anvesion'))

from text_normalizer import normalize_corpus
from db import resultsCollection as r
import numpy as np

#fetch all contents from db
results = r.find()
word_dictionary = dict() # stores word count
tokenized_text = [] # stores documents as keys
raw_text = [] # documents

class Index:
    '''
        An index is a node in a tree.
        node has name, branches -> nextIndexes, and value -> documents 
    '''
    def __init__(self):
        self.name = None
        self.nextIndexes = []
        self.documents = []

    def __str_(self):
        return "name: {}, next: {}, documents: {}".format(self.name, [s.name for s in self.nextIndexes], self.documents)

#sort tokenized_text by frequency(keys)
def sortByFrequency(e):
    return word_dictionary[e]


def iterateIndex(index, text, num):
    '''
        iterate over index tree till required node is found
        and create a new node as branch if found node.
    '''
    if index.name != text[0]:
        return False
    if len(text)>1:
        iterated = []

        #iterate over all the branches
        for n in index.nextIndexes:
            iterated.append(iterateIndex(n, text[1:], num))

        if not any(iterated):
            index.nextIndexes.append(createIndex(index, text[1:], num))
    return True

def createIndex(parentIndex, text, num):
    '''
        creates a new node for each key(text)
    '''
    index = Index()
    index.name = text[0]
    if len(text)>1:
        index.nextIndexes.append(createIndex(index, text[1:], num))
    else:
        index.documents = raw_text[num-1]
        #print(index)
    return index


headIndex = Index()
headIndex.name = 'HeadIndex'
num = 0

#text processing too convert text -> list of keys
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

print("Creating Index")

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
    '''
        extract documents with given index
    '''
    global documents
    if len(index.documents)>0:
        documents.append(index.documents)
    for n in index.nextIndexes:
        extractDocument(n)
    

def searchIndexedContent(index, token):
    '''
        search all indexes for the given token
    '''
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
