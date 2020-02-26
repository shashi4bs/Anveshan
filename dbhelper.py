import pymongo
#from AnveshanCrawler.constants import MONGODB_LINK

MONGODB_LINK = "mongodb://localhost:27017/"
class DBConnection(object):
    def __init__(self, DBNAME='AnveshanDB'):
        self.dbname = DBNAME
        self.collections = ['index_url_map', 'content']

    def get_content_by_index(tokens):
        
