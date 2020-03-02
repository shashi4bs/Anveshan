import math

class BM25(object):
    def __init__(self, query, k1=1.5, b=0.75, epsilon=0.25):
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon
        self.query = query
        self.idf = []
        self.score = {}

    def get_relevance_score(self, index_search_result, content_search_result):
        for i, index in enumerate(self.query.keys()):
            print(index_search_result[i][index])

        #idf = N/n => No of docs in corpus/ no of documents where term t is present
        total_retrieved_docs = len(content_search_result) #N
        for i, index in enumerate(self.query.keys()):
            self.idf.append(
            math.log(total_retrieved_docs / len(index_search_result[i][index]))
            ) #log(N/n)
        
        #calculate score for each doc
        avg_len = sum([doc['doc_length'] for doc in content_search_result])/total_retrieved_docs

        def get_term_frequency(term, index):
            #extract term frequency from index_search_result
            for i in index_search_result:
                if index in i.keys():
                    for urls in i[index]:
                        if urls[0] == term:
                            return urls[1]
            return 1

        for doc in content_search_result:
            score = 0
            for i, index in enumerate(self.query.keys()):
                tf = get_term_frequency(doc['url'], index)
                score += self.idf[i] * (tf * ( self.k1 + 1))/\
                (tf + self.k1 * (1 - self.b + (self.b * doc['doc_length']/avg_len)))
            self.score.update({doc['url']: score})

        return self.score
