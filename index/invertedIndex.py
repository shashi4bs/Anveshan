import sys
import os
sys.path.append(os.path.abspath('../Anvesion'))

from text_normalizer import normalize_corpus
from db import resultsCollection as r, invertedIndex

results = r.find()

for res in results:
    id_ = res["_id"]
    text = res["text"]
    author = res["author"]
    tags = res["tags"]
    print('Id: {}, text: {}, author: {}, tags: {}'.format(id_, text, author, tags))
