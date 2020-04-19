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

def normalize_score(score):
    #score -> data type -> dict
    max_score = max(score.values())
    min_score = min(score.values())
    for index in score:
        score[index] = (score[index] - min_score) / (max_score - min_score)
    return score

def combine_score(bm25_score, pr_score):
    score = {}
    pr_score = normalize_score(pr_score)
    bm25_score = normalize_score(bm25_score)
    for index in bm25_score:
        score[index] = bm25_score[index] + pr_score[index]

    return score

        
