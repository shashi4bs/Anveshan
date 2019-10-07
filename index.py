from db import resultsCollection as r
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

result = r.find() #fetch all from db.results

word_dictionary = dict()

ps = PorterStemmer() #for stemming

tokenized_text = []
raw_text = []
for res in result:
    text = word_tokenize(res["text"][0])
    text = [ps.stem(t) for t in text]
    for t in text:
        if t not in word_dictionary.keys():
            word_dictionary[t] = 1
        else:
            word_dictionary[t] += 1
    raw_text.append(res["text"][0])
    text = list(set(text)) #extract unique elements from text
    tokenized_text.append(text)
keys = sorted(word_dictionary.items(), key=lambda x:(x[1], x[0]), reverse=True)
#print(sorted(word_dictionary.items()))
#print(len(word_dictionary.keys()))

class Index:
    def __init__(self):
        self.name = None
        self.nextIndexes = [] 
        self.documents = []

    def __str__(self):
        return "name: {}, next: {}, documents: {}".format(self.name, [s.name for  s in self.nextIndexes], self.documents)

headIndex = Index()
headIndex.name = "HeadIndex"
#print(keys)
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

num = 0
for t in tokenized_text:
    sorted_t = sorted(t, key=sortByFrequency, reverse=True)
    if len(headIndex.nextIndexes) is 0:
        headIndex.nextIndexes.append(createIndex(headIndex, sorted_t, num))
        num += 1
        #print(headIndex, num)
    else:
        num += 1
        #print(headIndex, num)
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

#search("die")
