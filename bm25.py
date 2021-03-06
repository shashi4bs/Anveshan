import math

class BM25(object):
    def __init__(self, query, k1=1.5, b=0.75, epsilon=0.25):
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon
        self.query = query
        self.idf = {}
        self.score = {}

    def _get_idf(self, results):
        #idf = log(N/n) => No of docs in corpus/ no of documents where term t is present
        total_retrieved_documents = len(results) #N
        

        #initialise idf for each index = 0
        for q in self.query:
            self.idf[q] = 0
        #calculate idf for each retrived document
        for result in results:
            for q in self.query:
                #using self.idf to trace no of documents where term t appears
                if q in result['index']:
                    self.idf[q] += 1

        #calculate idf for each query tokens
        #using idf = log(1 + N/n)
        for q in self.query:
            self.idf[q] = math.log(1 + \
            (total_retrieved_documents / self.idf[q]))
        return self.idf

    def get_relevance_score(self, results):
        
        #self.idf = _get_idf(results)
        self._get_idf(results)
        
        #calculate relevance score
        #refering bm25 calculation method - https://en.wikipedia.org/wiki/Okapi_BM25
        avg_doc_len = sum([result['doc_length'] for result in results])/len(results)

        score = {}
        for result in results:
            score_D_Q = 0
            for index in result['index']:
                #f_qi_d = no of times term qi appeared in document d 
                count_index = result['index'].index(index)
                f_qi_d = result['count'][count_index]
                d_by_avgdl = result['doc_length'] / avg_doc_len
                
                score_D_Q += (self.idf[index] * (\
                    (f_qi_d * (self.k1 + 1))/\
                    (f_qi_d + self.k1 * (1 - self.b +self.b * d_by_avgdl))
                ))
            score[result['url']] =  score_D_Q

        #print(score)
        return score
