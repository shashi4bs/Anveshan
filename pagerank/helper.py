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
    
    '''
    links = list()
    edges = []

    # to generate for links only in content search result
    for content in content_search_result:
        links.append(content['url'])
    print("Generating Graph for {} links".format(len(links)))
    
    print("Generating Nodes")
    graph.add_nodes_from([_ for _ in range(len(links))])
   
    print("Adding edges")
    for content in content_search_result:
        for link in content['links']:
            if link in links:
                edges.append((links.index(content['url']), links.index(link)))
    
    print(edges)
    '''
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
    '''       
    for content in content_search_result:
        url = content['url']
        for c in content_search_result:
            if url in c['links']:
                edges.add((links.index(content['url']), links.index(url)))
    '''
    edges = list(edges)
    print(edges)
    graph.add_edges_from(edges)
    return graph, links
