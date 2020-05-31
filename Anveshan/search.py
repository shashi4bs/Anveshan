from mongo.mongodump import MongoPipeline
from text_normalizer import Tokenizer
from bm25 import BM25
from helper import combine_index_content_result, combine_score
from pagerank.pagerank import PageRank
from pagerank.graph import Graph
from pagerank.helper import get_personalization_vector 
from utils.resource_utils import save_personalization_vector
from flask_login import current_user

class Search(object):
    def __init__(self, generate_pr_score=True):
        self.db = MongoPipeline('AnveshanDB')
        self.content = self.db.get_content()
        self.graph = Graph(self.content)
        if generate_pr_score:
            personalization_vector = get_personalization_vector(self.graph.graph, self.content)
            self.pr = PageRank(self.graph, personalization=personalization_vector)
            print("calc pr")
            pr_score = self.pr.get_score()
            print("Saving pr to db")
            self.db.save_pr_score(pr_score)
            #save persoanlization vector in db
            save_personalization_vector(personalization_vector)
        else:
            self.pr = PageRank(
            graph = self.graph,\
            score = self.db.get_pr_score())
       
        #print(self.pr)
        #print(self.graph.get_adjacency_matrix())
        
    def search(self, query, user_resource=None):
        self.index_search_result = dict()
        self.content_search_result = dict()
        #tokenizer = Tokenizer()
        #query_tokens = tokenizer.processItem(query)
        query_tokens = query.true_tokens
        print(query.token_weights)
        self.index_search_result, self.content_search_result = self.db.get_content_by_index(query_tokens, query.token_weights)
        print(len(self.index_search_result), len(self.content_search_result))
        
        combined_result = combine_index_content_result(\
            self.index_search_result,\
            self.content_search_result\
        )
        bm25 = BM25(query_tokens)
        #print("tokens", query_tokens)

        #print("combined result", combined_result)
        
        #bm25 get_relevance_score for combined result
        score = bm25.get_relevance_score(combined_result)
        
        #pagerank
        if user_resource is None:
            pr_score = self.pr.get_score_for_search(self.content_search_result)
            combined_score = combine_score(score, pr_score)
        else:
            user = current_user
            pr_score = PageRank.filter_score_from_pr_score(self.content_search_result, user_resource["pr_score"])
            combined_score = combine_score(score, pr_score, pr=user.pr, bm25 = user.bm25)
        #print(user_resource, pr_score)
        #combined_score = combine_score(score , pr_score)
 
        def get_score(content):
            print(content['url'], ": BM25 : ", score[content['url']], "PR: ", pr_score[content['url']])
            return combined_score[content['url']]
 
        
        return sorted([content[0] for content in self.content_search_result], key=get_score, reverse=True)

    def personalized_search(self, query, user_resource, personalization=True):
        user = current_user
        print("pr: ",user.pr, "bm25: ", user.bm25)
        #user resource contain user specific pr_score, and personalization_vector
        print("personalization", personalization)
        if personalization:
            return self.search(query, user_resource)
        else:
            return self.search(query)



class result(object):
    def __init__(self, url, title):
        self.url = url
        self.title = title
