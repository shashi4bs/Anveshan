import math
from text_normalizer import Tokenizer
from config import TAGWEIGHT

tokenizer = Tokenizer()

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
            (total_retrieved_documents / (self.idf[q] + 0.1)))
        return self.idf

    def get_relevance_score(self, results, tags=None):
        
        #self.idf = _get_idf(results)
        self._get_idf([r[0] for r in results])
        
        #calculate relevance score
        #refering bm25 calculation method - https://en.wikipedia.org/wiki/Okapi_BM25
        avg_doc_len = sum([result[0]['doc_length'] for result in results])/len(results)

        score = {}
        for (result, w) in results:
	    #w -> query token weight
            #if query contains title of page assign title score
            title_score = self.get_score_for_title(result)
            #add tag bias on bm25 score
            processed_tags = []
            if tags and len(tags)>0:
                for t in tags:
                    for p_t in tokenizer.processItem(t):
                        processed_tags.append(p_t)


            #print(processed_tags)

            score_D_Q = 0
            for index in result['index']:
                #f_qi_d = no of times term qi appeared in document d 
                count_index = result['index'].index(index)
                f_qi_d = result['count'][count_index]
                d_by_avgdl = result['doc_length'] / avg_doc_len
                
                score_D_Q += (self.idf[index] * (\
                    (f_qi_d * (self.k1 + 1))/\
                    (f_qi_d + self.k1 * (1 - self.b +self.b * d_by_avgdl))
                )) * w

                #add tag bias here
                if index in processed_tags:
                    score_D_Q += TAGWEIGHT
            score[result['url']] =  score_D_Q + title_score

        #print(score)
        return score
    
    def get_score_for_title(self, result):
        #process content in title
        for t in result['title']:
            tokens = tokenizer.processItem(t)
            for token in tokens:
                if token in self.query:
                    return self.query[token] * (self.k1 + self.b + self.epsilon * 100)

        return 0

