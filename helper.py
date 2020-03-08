def combine_index_content_result(index_result, content_result):
    result = []
    for content in content_result:
        res = {
        'url': content['url'],
        'title': content['title'],
        'index': [],
        'count': [],
        'doc_length': content['doc_length']
        }
        for index in index_result:
            idx_list = list(index.keys())
            idx_list.remove('_id')
            idx = idx_list[0]
            
            for url, count in index[idx]:
                if content['url'] == url:
                    res['index'].append(idx)
                    res['count'].append(count)
                    break
        print(res)
        result.append(res)
        
    return result
