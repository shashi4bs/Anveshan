from mongo.resources import AnveshanResource
import networkx as nx

anveshan_resource = AnveshanResource()

def allocate_resource_for_user(user):
    print(user.username)
    #load defaultGraph #name->DefaultGraph
    json_graph, links = anveshan_resource.load_graph("DefaultGraph")
    anveshan_resource.save_graph(json_graph, links, user.username) 
    return

def load_user_resource(user):
    json_graph, links = anveshan_resource.load_graph(user.username)
    graph = nx.node_link_graph(json_graph)
    return {"graph": graph, "links": links}
