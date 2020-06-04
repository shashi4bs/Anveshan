from mongo.resources import AnveshanResource
from db import UserContributions 

class UserContrib(AnveshanResource):
    def __init__(self, db_name="AnveshanUser"):
        AnveshanResource.__init__(self, db_name)
        
    def save_index(self, index, item):
        try:
            query = {index : {'$exists' : 'true'}}
            result = self.index_url_map.find(query)
            num_entries = result.count()
            if num_entries == 0:
                insert_query = {
                    index: [item]
                }
                self.index_url_map.insert(insert_query)
            else:
                update_query = {index : item}
                for r in result:
                    self.index_url_map.update(                  
                        {'_id' : r['_id']},
                        {'$addToSet' : update_query})
        except Exception as e:
            print(e)

    def save_content(self, content, url, username):
        #content type dict
        for index in content:
            item = [url, content[index]]
            self.save_index(index, item)
        #update verify flasg
        user_contrib = UserContributions.query.filter(UserContributions.username == username).first()
        user_contrib.verified = True
        user_contrib.save()
        
