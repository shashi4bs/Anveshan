import re

def make_full_links(links, base):
    full_links = []
    for link in links:
        if re.search("^http", link):
            pass
        else:
            full_links.append(base+link)
    return full_links
    
def make_content_matrix(content, max_cols=50):
    #content -> dict(key-> token, value-> frequency)
    content_matrix = list()
    sorted_content = sorted(content.items(), key=lambda item: item[1], reverse=True)
    content_matrix = [c[0] for c in sorted_content]
    
    if len(content_matrix) > max_cols:
        content_matrix = content_matrix[:50]
    print(content_matrix)
    return content_matrix
