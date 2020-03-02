from mongodump import MongoPipeline
from text_normalizer import Tokenizer
from bm25 import BM25

class Search(object):
    def __init__(self):
        self.db = MongoPipeline('AnveshanDB')
        
    def search(self, query):
        self.index_search_result = dict()
        self.content_search_result = dict()
        tokenizer = Tokenizer()
        query_tokens = tokenizer.processItem(query)
        self.index_search_result, self.content_search_result = self.db.get_content_by_index(query_tokens)
        
        #[print(i['title']) for i in self.content_search_result]
        #[print(i) for i in self.index_search_result]

        bm25 = BM25(query_tokens)
        score = bm25.get_relevance_score(self.index_search_result, self.content_search_result)
        print(score)

        def get_score(content):
            return score[content['url']]
         
        return sorted(self.content_search_result, key=get_score, reverse=True)

class result(object):
    def __init__(self, url, title):
        self.url = url
        self.title = title
