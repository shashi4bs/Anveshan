from mongo.resources import AnveshanResource
from mongo.mongodump import MongoPipeline
import networkx as nx

anveshan_resource = AnveshanResource()
mongopipeline = MongoPipeline()

def allocate_resource_for_user(user):
    print(user.username)
    #load defaultGraph #name->DefaultGraph
    json_graph, links = anveshan_resource.load_graph("DefaultGraph")
    #load default pr_score
    pr_score = mongopipeline.get_pr_score()

    #save graph for user
    anveshan_resource.save_graph(json_graph, links, user.username)
    #save pr_score for user
    anveshan_resource.save_pr_score(pr_score, user.username)
    return

def load_user_resource(user):
    json_graph, links = anveshan_resource.load_graph(user.username)
    graph = nx.node_link_graph(json_graph)
    pr_score = anveshan_resource.get_pr_score(user.username)
    return {"graph": graph, "links": links, "pr_score": pr_score}
