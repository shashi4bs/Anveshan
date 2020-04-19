import networkx as nx
from pagerank.helper import generate_graph, check_graph_for_consistency, make_graph_consistent
from mongo.resources import AnveshanResource
import traceback

global anveshan_resource
anveshan_resource = AnveshanResource()

class Graph():
    def __init__(self, content_search_result):
        try:
            self.load()
            is_graph_consistent = check_graph_for_consistency(self.links, content_search_result)
            print(is_graph_consistent)
            if not is_graph_consistent:
                self.graph, self.links = make_graph_consistent(self.graph, self.links, content_search_result)
                self.save()
        except Exception as e:
            print(e)
            traceback.print_exc()
            self.graph, self.links = generate_graph(content_search_result)
            self.save()

    def get_adjacency_matrix(self, sparse=True):
        if sparse:
            #return scipy sparse matrix
            return nx.adjacency_matrix(self.graph)
        else:
            #return numpy adjacency matrix
            return nx.to_numpy_matrix(self.graph)

    def save(self, name="DefaultGraph"):
        graph_to_json = nx.node_link_data(self.graph)
        #save to db anveshan resources
        anveshan_resource.save_graph(graph_to_json, self.links, name)

    def load(self, name="DefaultGraph"):
        #load json graph data from anveshan resources
        json_graph, self.links = anveshan_resource.load_graph(name)
        self.graph = nx.node_link_graph(json_graph)
        
