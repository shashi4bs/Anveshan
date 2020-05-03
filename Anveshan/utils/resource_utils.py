from mongo.resources import AnveshanResource
from mongo.mongodump import MongoPipeline
import networkx as nx
from bson import ObjectId
from pagerank.pagerank import PageRank
from pagerank.graph import Graph
import json

anveshan_resource = AnveshanResource()
mongopipeline = MongoPipeline()

def generate_personalization_vector(links):
    p_vector = dict()
    i = 0
    val = 1/len(links)
    for link in links:
        p_vector[i] = val
        i += 1
    return p_vector

def allocate_resource_for_user(user):
    print(user.username)
    #load defaultGraph #name->DefaultGraph
    #json_graph, links = anveshan_resource.load_graph("DefaultGraph")
    
    #load default pr_score
    pr_score = mongopipeline.get_pr_score()
    #load default p_vector
    p_vector = anveshan_resource.load_pvector("Default")
    
    #generate_personalization_vector
    #p_vector = generate_personalization_vector(links)
    #save graph for user
    #anveshan_resource.save_graph(json_graph, links, user.username)
    #save pr_score for user
    anveshan_resource.save_pr_score(pr_score, user.username)
    #save p_vector
    anveshan_resource.save_pvector(p_vector, user.username)
    #anveshan_resource.save_pvector(p_vector, "Default")
    return

def load_user_resource(user):
    #json_graph, links = anveshan_resource.load_graph(user.username)
    #graph = nx.node_link_graph(json_graph)
    pr_score = anveshan_resource.get_pr_score(user.username)
    p_vector = anveshan_resource.load_pvector(user.username)
    return {"pr_score": pr_score, "p_vector" : p_vector}


def get_tag_from_content(_id):
    query = {'_id' : ObjectId(_id)}
    result = mongopipeline.content.find(query)
    print(result)
    for r in result:
        return r["tags"]

def update_weights(graph, tags, user, user_resources, urls):
    #extract links with tag = tags
    query = {'tags' : tags}
    links = []
    p_vector = user_resources["p_vector"]
    pr_score = user_resources["pr_score"]
    result = mongopipeline.content.find(query)

    for res in result:
        links.append(res["url"])
    p_vector = dict()
    #modify p_vector
    for link in links:
        index = str(urls.index(link))
        if(pr_score[link] < 0.8):
            pr_score[link] += 0.1
        p_vector[index] = 1
    
    print("Generating personalized pr_score")
    
    print(graph)

    
    #generate pr_score
    #pr = nx.pagerank(graph, personalization=p_vector) 
    #modify pr
    #pr = PageRank.make_pr_score(pr, urls)
    #print(pr)
    #print(p_vector)
    #save pr_score
    anveshan_resource.save_pr_score(pr_score, user.username)
    #save p_vector
    anveshan_resource.save_pvector(p_vector, user.username)
    return
    
