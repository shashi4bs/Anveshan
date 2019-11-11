def sortByScore(searchResults, tfidfScore):
    sortedResult = []
    to_remove = [] # sorted documents to be removed from searchResults
    for _ in range(len(searchResults)):
        index = 0
        
        if max(tfidfScore)>0:
            while tfidfScore[index] != max(tfidfScore):
                index += 1
            tfidfScore[index] = 0
            sortedResult.append(searchResults[index])
            to_remove.append(searchResults[index])
    # removing sorted results 
    for r in to_remove:
        searchResults.remove(r)

    # if any document exits with tfidfScore 0
    if len(searchResults) > 0:
        sortedResult.extend(searchResults)
    return sortedResult
