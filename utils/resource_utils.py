from mongo.resources import AnveshanResource
from mongo.mongodump import MongoPipeline
import networkx as nx
from bson import ObjectId
from pagerank.pagerank import PageRank
from pagerank.graph import Graph

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


def get_tag_from_content(_id):
    query = {'_id' : ObjectId(_id)}
    result = mongopipeline.content.find(query)
    print(result)
    for r in result:
        return r["tags"]

def update_weights(tags, user, user_resources):
    #extract links with tag = tags
    query = {'tags' : tags}
    links = []
    result = mongopipeline.content.find(query)

    for res in result:
        links.append(res["url"])

    #add personalization
    personalization = dict()
    print("generating personalization for {} links {}".format(len(user_resources["links"]), len(links)))
    for link in user_resources['links']:
        if link in links:
            personalization[user_resources["links"].index(link)] = 1
        else:
            personalization[user_resources["links"].index(link)] = 0
    
    print("Generating personalized pr_score")
    #generate pr_score
    pr = nx.pagerank(user_resources["graph"], personalization=personalization)
    
    #save pr_score

    #anveshan_resource.save_pr_score(pr, user.username)
    return pr
    
    
