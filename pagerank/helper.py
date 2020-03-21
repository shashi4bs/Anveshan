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
    graph.add_nodes_from([_ for _ in range(len(links))])

    print("Adding Edges")
    
    processed = 0
    for content in content_search_result:
        print("Adding edges : ", processed)
        processed += 1
        for l in content['links']:
            #add content['links'] -> content['url']
            edges.add((links.index(l), links.index(content['url'])))
    
    edges = list(edges)
    print(edges)
    graph.add_edges_from(edges)
    return graph, links

def extract_links(content_search_result):
    content_links = set()
    for content in content_search_result:
        content_links.add(content['url'])
        [content_links.add(link) for link in content['links']]

    return list(content_links)

def check_graph_for_consistency(links, content_search_result):
    
    content_links = extract_links(content_search_result)

    if len(links) != len(content_links):
        return False
    else:
        return True

def make_graph_consistent(graph, links, content_search_result):
    content_links = extract_links(content_search_result)

    if len(links) != len(content_links):
        node_list = list(graph.nodes)
        max_node = max(node_list)
        
        new_nodes_to_add = []
        for i in range(1, len(content_links) - len(links) + 1):
            new_nodes_to_add.append(max_node + i)
        graph.add_nodes_from(new_nodes_to_add)

        new_edges = set()
        
        #extract new links
        new_links = list(set(content_links) - set(links))
        links.extend(new_links)
        for content in content_search_result:
            if content['url'] in new_links:
                for l in content["links"]:
                    new_edges.add((links.index(l), links.index(content["url"])))
        new_edges = list(new_edges)
        graph.add_edges_from(new_edges)
    
    return graph, links
