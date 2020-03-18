from pagerank.helper import generate_pr_matrix, generate_graph
import networkx as nx

class PageRank(object):
    def __init__(self, graph, score=None, alpha=0.99):
        #print("Generating PageRank Matrix")
        #self.pr_matrix = generate_pr_matrix(content_search_result)
        #self.graph, self.links = generate_graph(content_search_result)
        self.graph = graph.graph
        self.links = graph.links
        self.alpha = alpha
        if score:
            self.pr = score
        else:
            self.pr = nx.pagerank(self.graph, \
                                alpha=alpha,\
                                max_iter=10,\
                                tol=1e-03)

    def get_score(self):
        #pr = nx.pagerank(self.graph, self.alpha)
        score = {}
        index = 0
        for link in self.links:
            score[link] = self.pr[index]
            index += 1

        return score

    def get_score_for_search(self, content_search_result):
        score = {}
        for content in content_search_result:
            score[content['url']] = self.pr[content['url']]
        return score
