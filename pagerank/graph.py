import networkx as nx
from pagerank.helper import generate_graph


class Graph(object):
    def __init__(self, content_search_engine):
        self.graph, self.links = generate_graph(content_search_engine) 
