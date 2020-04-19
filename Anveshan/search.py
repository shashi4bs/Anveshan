from mongo.mongodump import MongoPipeline
from text_normalizer import Tokenizer
from bm25 import BM25
from helper import combine_index_content_result, combine_score
from pagerank.pagerank import PageRank
from pagerank.graph import Graph

class Search(object):
    def __init__(self, generate_pr_score=True):
        self.db = MongoPipeline('AnveshanDB')
        self.content = self.db.get_content()
        self.graph = Graph(self.content)
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
       
        #print(self.pr)
        #print(self.graph.get_adjacency_matrix())
        
    def search(self, query, user_resource=None):
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
        if user_resource is None:
            pr_score = self.pr.get_score_for_search(self.content_search_result)
        else:
            pr_score = PageRank.filter_score_from_pr_score(self.content_search_result, user_resource["pr_score"])
        print(user_resource, pr_score)
        combined_score = combine_score(score , pr_score)
 
        def get_score(content):
            print(content['url'], ": BM25 : ", score[content['url']], "PR: ", pr_score[content['url']])
            return combined_score[content['url']]
 
        
        return sorted(self.content_search_result, key=get_score, reverse=True)

    def personalized_search(self, query, user_resource):
        #user resource contain user specific pr_score, and personalization_vector
        return self.search(query, user_resource)


class result(object):
    def __init__(self, url, title):
        self.url = url
        self.title = title
