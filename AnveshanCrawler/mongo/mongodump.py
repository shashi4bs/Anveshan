import pymongo
from constants import MONGODB_LINK
import numpy as np
import json

class MongoPipeline(object):
    def __init__(self, db_name="AnveshanDB"):
        mongo_client = pymongo.MongoClient(MONGODB_LINK) 
        self.db = mongo_client[db_name]
        self.index_url_map = self.db["index_url_map"]
        self.content = self.db["content"]
        self.pr_score = self.db["pr_score"]
    

    def __save_index(self, index, item):
        
        try:
            query = {index : {'$exists' : 'true'}}
            result = self.index_url_map.find(query)
            num_entries = result.count()
            if num_entries == 0:
                insert_query = {index: [[item['url'], item['content'][index]]]}
                self.index_url_map.insert_one(insert_query)
            else:
                update_query = {index: [item['url'], item['content'][index]]}
                for r in result:
                    self.index_url_map.update(
                        {'_id': r['_id']},
                        {'$addToSet': update_query}
                    )
            print('SAVED : {}'.format(query))
        except Exception as e:
            print("Exception in saving index : {}".format(index))
            print(e)



    def save(self, item):
        print("save invoked from MogoPipeline")
        #save index - url mapping
        
        for index in item['content']:
            self.__save_index(index, item)  
        
        #index from title
        for index in item['title']:
            self.__save_index(index, item)

        #save url content
        query = {'url': item['url']} 
        num_entries = self.content.find(query).count()
        if num_entries == 0:
            insert_query = {'url': item['url'], 'title': item['title'], 'links':item['links'], 'doc_length': sum(item['content'].values())}
            self.content.insert_one(insert_query)
            print("Saved : {}".format(insert_query))
        else:
            pass
        #id_ = self.db.insert_one()
        print("Saved ID")
        

    def get_content_by_index(self, tokens):
        index_search_result = []
        content_search_result = []
        for token in tokens:
            query = {token: {'$exists': 'true'}}
            result = self.db.index_url_map.find(query)
            [index_search_result.append(r) for r in result]

        #search content for url
        for r in index_search_result:
            #iterate over dict keys except _id
            for urls in list(r.values())[1:]:
                #search content over unique list of urls
                for url in set(np.array(urls)[:, 0]):
                    query = {'url': url}
                    result = self.db.content.find(query)
                    [content_search_result.append(r) for r in result]
        return index_search_result, content_search_result

    def get_content(self):
        content_search_result = []
        result = self.db.content.find()
        [content_search_result.append(r) for r in result]
        return content_search_result

    '''
    def save_pr_score(self, pr_score):
        print(pr_score)
        for link in pr_score:
            query = {"link" : link}
            result = self.db.pr_score.find(query)
            if result.count() == 0:
                insert_query = {"link": link, "score": pr_score[link]}
                self.db.pr_score.insert_one(insert_query)
            else:
                update_query = {"score": pr_score[link]}
                for r in result:
                    self.db.pr_score.update(
                        {'_id':r['_id']},
                        {'$set': update_query}
                    )
        print("Page Rank Score Saved")                
    '''

    def save_pr_score(self, pr_score):
        print("Storing {} entries in db".format(len(pr_score.keys())))
        query = {"pr": {"$exists": "true"}}
        pr = self.db.pr_score.find(query)
        if pr.count() == 0:
            self.db.pr_score.save({
            "pr": json.dumps(pr_score) 
            })
        else:
            for p in pr:
                self.db.pr_score.update(
                    {'_id': p['_id']},
                    {'$set':  {"pr" : json.dumps(pr_score)}}
                )
                
        print("PageRank saved in db")

    def get_pr_score(self):
        query = {"pr": {"$exists": "true"}}

        pr = self.db.pr_score.find(query)
        for p in pr:
            return json.loads(p["pr"])
