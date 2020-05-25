from mongo.resources import AnveshanResource
from mongo.mongodump import MongoPipeline
#from pagerank.pagerank import Pagerank
from pagerank.helper import get_transformation_matrix
import numpy as np
from db import User

anveshan_resource = AnveshanResource()
mongopipeline = MongoPipeline()

def get_personalization_vector(graph, contents=None):
    links = list(graph.nodes)
    personalization = dict()
    for link in links:
        personalization[link] = 0.2
    if contents:
        for content in contents:
            url = content["url"]
            personalization[url] = 0.5

    return personalization

def update_resources(graph, links, content_search_result):
    #generate new default p_vector
    personalization = get_personalization_vector(graph, content_search_result)
    
    #update p_r score for all

    #pagerank = PageRank(graph, personalization=personalization)
    tr_matrix = get_transformation_matrix(graph, alpha=0.9, nodelist=graph.nodes, personalization=personalization)
    link_prob = [1 for _ in range(len(list(graph.nodes)))]
    score = np.matmul(link_prob, tr_matrix)/len(personalization)
    score = np.ravel(score)

    pr_score = {}
    for url, s in zip(list(graph.nodes), score):
        pr_score[url] = s

    #update default pagerank score
    mongopipeline.save_pr_score(pr_score)

    #read all user
    users = User.query.all()
    for user in users:
        username = user.username
        #read p_vector
        p_vector = anveshan_resource.load_pvector(username)
        #update p_vector
        for url in personalization:
            if url not in p_vector.keys():
                p_vector[url] = personalization[url]

        #calculate pr_score
        tr_matrix = get_transformation_matrix(graph, alpha=0.9, nodelist=graph.nodes, personalization=p_vector)
        link_prob = [1 for _ in range(len(list(graph.nodes)))]
        score = np.matmul(link_prob, tr_matrix)/len(personalization)
        score = np.ravel(score)

        pr_score = {}
        for url, s in zip(list(graph.nodes), score):
            pr_score[url] = s


        #save pr_score
        anveshan_resource.save_pr_score(pr_score, username)
        #save p_vector
        anveshan_resource.save_pvector(p_vector, username)

    return 




'''
def update_resources(graph, links, content_search_result):
    #generate new default p_vector
    personalization = get_personalization_vector(graph, content_search_result)
    
    #update p_r score for all

    #pagerank = PageRank(graph, personalization=personalization)
    tr_matrix = get_transformation_matrix(graph, alpha=0.9, nodelist=graph.nodes, personalization=personalization)
    link_prob = [1 for _ in range(len(list(graph.nodes)))]
    score = np.matmul(link_prob, tr_matrix)/len(personalization)
    score = np.ravel(score)

    pr_score = {}
    for url, s in zip(list(graph.nodes), score):
        pr_score[url] = s

    #update default pagerank score
    mongopipeline.save_pr_score(pr_score)

    #update pr_score and p_vector for each user
    p_vectors = []
    #read all p_vector
    result = anveshan_resource.p_vector.find()
    for res in result:
        del res['_id']
        p_vectors.append(res)


    for p_vector in p_vectors:
        for username in p_vector:
            if username == "default":
                continue
            p_vector = p_vector[username]
            #update p_vector
            for url in personalization:
                if url not in p_vector.keys():
                    p_vector[url] = personalization[url]

            #update pr_score
            #pagerank = PageRank(graph, personalization=p_vector)
            tr_matrix = get_transformation_matrix(graph, alpha=0.9, nodelist=graph.nodes, personalization=p_vector)
            link_prob = [1 for _ in range(len(list(graph.nodes)))]
            score = np.matmul(link_prob, tr_matrix)/len(personalization)
            score = np.ravel(score)
            pr_score = {}
            for url, s in zip(list(graph.nodes), score):
                pr_score[url] = s
            
            #save pr_score
            anveshan_resource.save_pr_score(pr_score, username)
            #save p_vector
            anveshan_resource.save_pvector(p_vector, username)

    return  
'''
