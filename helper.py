def sortByScore(searchResults, tfidfScore):
    sortedResult = []
    for _ in range(len(searchResults)):
        index = 0
        while tfidfScore[index] != max(tfidfScore):
            index += 1
        tfidfScore[index] = 0
        sortedResult.append(searchResults[index])
    return sortedResult
