import pymongo
from constants import MONGODB_LINK


class MongoPipeline(object):
    def __init__(self, db_name="AnveshanDB"):
        mongo_client = pymongo.MongoClient(MONGODB_LINK) 
        self.db = mongo_client[db_name]
        self.index_url_map = self.db["index_url_map"]
        self.content = self.db["content"]
    

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
        result = []
        for token in tokens:
            query = {token: {'$exists': 'true'}}
            r = self.db.index_url_map.find(query)
            result.append(r)
        return result
