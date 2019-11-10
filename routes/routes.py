from app import seApp
from flask import request, jsonify
from db import resultsCollection
#from treeIndex import headIndex as index, searchToken
from index import treeIndex

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
        searchResults.append(result)
    '''
    for r in result:
        del r['_id']
        searchResults.append(r)
    '''
    #print(searchResults)
    return jsonify(searchResults)
