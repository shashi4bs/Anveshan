import numpy as np
import networkx as nx

def generate_pr_matrix(content_search_result):
    #generate page rank matrix (sparse)
    print(content_search_result[0].keys())
    links = set()
    for content in content_search_result:
        links.add(content['url'])
        [links.add(link) for link in content['links']]
    print(len(links))
    #casting link set to list
    links = list(links)
    
    pr_matrix = []
    
    processed = 0
    for content in content_search_result:
        #for links present on a specific page/url
        link_matrix = [0 for _ in links]
        for link in content['links']:
            index = links.index(link)
            link_matrix[index] = 1
        pr_matrix.append(link_matrix)
        processed += 1
        print("Completed processing {} link".format(processed))
    
    pr_matrix = np.array(pr_matrix)
    return pr_matrix

def trim_graph(graph, in_degree=0, out_degree=1):
    #drop nodes with in_degree 0 and outdegree 1
    print(len(list(graph.nodes)))
    in_degrees = graph.in_degree(graph)
    out_degrees = graph.out_degree(graph)
    removed = 0
    for n1, n2 in zip(in_degrees, out_degrees):
        if n1[1] == in_degree and n2[1] == out_degree:
            #remove node
            removed += 1
            graph.remove_node(n1[0])
    print(len(list(graph.nodes)))
    return graph, removed



def generate_graph(content_search_result):
    
    #graph = nx.Graph()
    
    #directed graph

    graph = nx.DiGraph()
    #to generate over all links
    links = set()
    edges = set()
    for content in content_search_result:
        links.add(content['url'])
        [links.add(link) for link in content['links']]

    
    links = list(links)

    
    print("Generating {}  Nodes".format(len(links)))
    #graph.add_nodes_from([_ for _ in range(len(links))])
    graph.add_nodes_from(links)

    print("Adding Edges")
    
    processed = 0
    for content in content_search_result:
        print("Adding edges : ", processed)
        processed += 1
        for l in content['links']:
            #add content['links'] -> content['url']
            #edges.add((links.index(l), links.index(content['url'])))
            edges.add((l, content['url']))

    edges = list(edges)
    #print(edges)
    graph.add_edges_from(edges)

    #trim graph
    graph, removed = trim_graph(graph)
    graph, removed = trim_graph(graph, 1, 0)
    print("Removed Node : ", removed)
    #print(graph.in_degree())
    #print(graph.out_degree())
    links = list(graph.nodes)

    return graph, links

def extract_links(content_search_result, extract_internal_links=False):
    content_links = set()
    for content in content_search_result:
        content_links.add(content['url'])
        if extract_internal_links:
            [content_links.add(link) for link in content['links']]

    return list(content_links)

def check_graph_for_consistency(links, content_search_result):
    
    content_links = extract_links(content_search_result)
    #search each url in content_links if it is present in links
    for link in content_links:
        if link not in links:
            return False

    return True


def make_graph_consistent(graph, links, content_search_result):
    content_links = extract_links(content_search_result, extract_internal_links=True)
        
    new_nodes_to_add = set()
    for link in content_links:
        if link not in links:
            new_nodes_to_add.add(link)
    
    new_nodes_to_add = list(new_nodes_to_add)
    #add new nodes to graph
    graph.add_nodes_from(new_nodes_to_add)

    new_edges = set()
    
    for content in content_search_result:
        #if content url is new
        if content['url'] in new_nodes_to_add:
            for link in content["links"]:
                new_edges.add((link, content["url"]))
    
    new_edges = list(new_edges)
    graph.add_edges_from(new_edges)
           
    #remove nodes with in_degree=0 outdegree = 1
    graph, removed = trim_graph(graph, 0, 0)
    graph, removed = trim_graph(graph)
    graph, removed = trim_graph(graph, 1, 0)
    links = list(graph.nodes)
    #update_resources(graph, links, content_search_result)
    return graph, links


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

def get_transformation_matrix(graph, alpha, nodelist, personalization):
    return nx.google_matrix(graph, alpha=alpha, nodelist=nodelist, personalization=personalization)
