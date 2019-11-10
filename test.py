from db import resultsCollection as r
from text_normalizer import normalize_corpus

results = r.find()

print(results)
for res in results:
    #print("Result: ", res)
    text = []
    text.extend(normalize_corpus(res["text"]))
    text.extend(normalize_corpus(res["author"]))
    text.extend(normalize_corpus(res["tags"]))
    print("Normalized Text: ", text)
