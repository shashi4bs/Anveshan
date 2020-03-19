from mongodump import MongoPipeline
from text_normalizer import Tokenizer
from bm25 import BM25
from helper import combine_index_content_result
from pagerank.pagerank import PageRank
from pagerank.graph import Graph

class Search(object):
    def __init__(self, generate_pr_score=True):
        self.db = MongoPipeline('AnveshanDB')
        self.graph = Graph(self.db.get_content())
        if generate_pr_score:
            self.pr = PageRank(self.graph)
            print("calc pr")
            pr_score = self.pr.get_score()
            print("Saving pr to db")
            self.db.save_pr_score(pr_score)
        else:
            self.pr = PageRank(
            graph = self.graph,\
            score = self.db.get_pr_score())
       
        print(self.pr)
        print(self.graph.get_adjacency_matrix())
        
    def search(self, query):
        self.index_search_result = dict()
        self.content_search_result = dict()
        tokenizer = Tokenizer()
        query_tokens = tokenizer.processItem(query)
        self.index_search_result, self.content_search_result = self.db.get_content_by_index(query_tokens)
        
        combined_result = combine_index_content_result(\
            self.index_search_result,\
            self.content_search_result\
        )
        bm25 = BM25(query_tokens)

        #bm25 get_relevance_score for combined result
        score = bm25.get_relevance_score(combined_result)
        
        #pagerank
        pr_score = self.pr.get_score_for_search(self.content_search_result)
         
        def get_score(content):
            return score[content['url']] + pr_score[content['url']]
         
        return sorted(self.content_search_result, key=get_score, reverse=True)

class result(object):
    def __init__(self, url, title):
        self.url = url
        self.title = title
