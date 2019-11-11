from app import seApp
from flask import request, jsonify
from db import resultsCollection
#from treeIndex import headIndex as index, searchToken
from index import treeIndex
from ranking.tfidf import score
from helper import sortByScore

print(treeIndex)
@seApp.route('/search')
def search():
    searchResults = []
    query = request.args.get("q")
    #query = '/'+query+'/i'
    #result = resultsCollection.find({"$text": {"$search": query}})
    for q in query.split():
        print(q)
        result = treeIndex.searchToken(q)
        searchResults.extend(result)
    searchResults = list(set(searchResults))
    tfidfScore = score(query, searchResults, treeIndex.tokenized_text)
    #sort by tfidfScore
    searchResults = sortByScore(searchResults, tfidfScore)
    return jsonify(searchResults)
