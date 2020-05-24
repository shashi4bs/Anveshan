from mongo.resources import AnveshanResource
from mongo.mongodump import MongoPipeline
import networkx as nx
from bson import ObjectId
from pagerank.pagerank import PageRank
from pagerank.graph import Graph
import json
import numpy as np
from pagerank.helper import get_transformation_matrix
#from db import User

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
    
    #load default pr_score
    pr_score = mongopipeline.get_pr_score()
    #load default p_vector
    p_vector = anveshan_resource.load_pvector("default")
    
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


def get_content(_id):
    query = {'_id' : ObjectId(_id)}
    result = mongopipeline.content.find(query)
    print("result ", result)
    for r in result:
        return r

def get_similar_contents(content_matrix):
    #read all contents from anveshandb
    content = mongopipeline.get_content()
    matrix = {}
    matrix_to_compare = [1 for _ in range(len(content_matrix))]
    for c in content:
        m = [0 for _ in range(len(content_matrix))]
        for tag in c["content_matrix"]:
            if tag in content_matrix:
                m[content_matrix.index(tag)] = 1
        matrix[c['url']] = m

    similarity_score = {}
    #calculate similarity
    for m in matrix:
        similarity_score[m] = np.dot(matrix_to_compare, matrix[m])/len(content_matrix)
    
    #print(similarity_score) 
    #filter content with score < 0.2
    similar_contents = {}
    threshhold = 0.2
    for url, score in similarity_score.items():
        if score > threshhold:
            similar_contents[url] = score
    return similar_contents

#def update_weights(graph, tags, user, user_resources, urls):
def update_weights(_id, username):
    content = get_content(_id)
    tag = content['tags']
    content_matrix = content["content_matrix"]
    #print(tag, content_matrix)
    similar_contents = get_similar_contents(content_matrix)

    query = {'tags' : tag}
    links = []
    #read p vector and pr_score
    p_vector = anveshan_resource.load_pvector(username)
    pr_score = anveshan_resource.get_pr_score(username)
    
    result = mongopipeline.content.find(query)

    for res in result:
        links.append(res["url"])

    #modify p_vector for tags
    for link in links:
        if(p_vector[link] < 0.9):
            p_vector[link] += 0.2

    #modify p_vector for similar content
    p_vector[content['url']] += 0.5
    for url in similar_contents:
        p_vector[url] += similar_contents[url]

    
    print("Generating personalized pr_score")
    #read graph
    #graph = anveshan_resource.load_graph("DefaultGraph")
    graph = Graph().graph
    #transformation matrix personalized for user
    tr_matrix = get_transformation_matrix(graph, alpha=0.9, nodelist=graph.nodes, personalization=p_vector)

    link_prob = [1 for _ in range(len(list(graph.nodes)))]
    score = np.matmul(link_prob, tr_matrix)/len(p_vector)
    score = np.ravel(score)

    pr_score = {}
    for url, s in zip(list(graph.nodes), score):
        pr_score[url] = s
    #print(pr_score)
    anveshan_resource.save_pr_score(pr_score, username)
    #save p_vector
    anveshan_resource.save_pvector(p_vector, username)
    return
    

def save_personalization_vector(personalization_vector, name="default"):
    anveshan_resource.save_pvector(personalization_vector, name)


