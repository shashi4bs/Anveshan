import networkx as nx
from pagerank.helper import generate_graph


class Graph(nx.Graph):
    def __init__(self, content_search_result):
        self.graph, self.links = generate_graph(content_search_result)

    def get_adjacency_matrix(self):
        return nx.adjacency_matrix(self.graph)
