from pagerank.helper import generate_pr_matrix, generate_graph, get_personalization_vector, get_transformation_matrix
import networkx as nx
import numpy as np


class PageRank(object):
    def __init__(self, graph, score=None, alpha=0.9, personalization=None):
        self.graph = graph.graph
        self.links = graph.links
        self.alpha = alpha
        if score:
            self.pr = score
        else:
            '''
            self.pr = nx.pagerank(self.graph, \
                                alpha=alpha,\
                                max_iter=10,\
                                tol=1e-03, 
                                personalization=personalization)
            '''
            if not personalization:
                personalization = get_personalization_vector(self.graph)
            self.tr_matrix = get_transformation_matrix(self.graph, alpha=alpha, nodelist=self.graph.nodes, personalization=personalization)
            #print(self.tr_matrix)
            link_prob = [1 for _ in range(len(list(self.graph.nodes)))]
            score = np.matmul(link_prob, self.tr_matrix)/len(personalization)
            score = np.ravel(score)
            #print(score)
            #print(score.shape)
            self.pr = {}
            
            for url, s in zip(list(self.graph.nodes), score):
                self.pr[url] = s
            

    def get_score(self):
        return self.pr

    def get_score_for_search(self, content_search_result):
        score = {}
        for (content, w) in content_search_result:
            score[content['url']] = self.pr[content['url']]
        return score

    @staticmethod
    def filter_score_from_pr_score(content_search_result, pr_score):
        score = {}
        for (content, w) in content_search_result:
            score[content['url']] = pr_score[content['url']]
        return score

    @staticmethod
    def make_pr_score(pr_score, links):
        score = {}
        test = []
        for index in pr_score:
            test.append(pr_score[index])
        print("test", max(test))
        for index in pr_score:
           score[links[index]] =  pr_score[index]
        return score
