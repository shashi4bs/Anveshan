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
    graph = nx.Graph()
    links = set()
    for content in content_search_result:
        links.add(content['url'])
        [links.add(link) for link in content['links']]
    links = list(links)
    print("Generating Graph for {} links".format(len(links)))
    
    print("Generating Nodes")
    graph.add_nodes_from([_ for _ in range(len(links))])

    print("Adding edges")
    edges = []
    processed_links = 0
    for content in content_search_result:
        link = links[processed_links]
        if link in content['links']:
            edges.append((processed_links, links.index(link)))
        processed_links += 1
        #print("Added edges for {} links".format(processed_links))

    graph.add_edges_from(edges)
    return graph, links
