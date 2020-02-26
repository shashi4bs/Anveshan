from mongodump import MongoPipeline
from text_normalizer import Tokenizer



class Search(object):
    def __init__(self):
        self.db = MongoPipeline('AnveshanDB')
        
    def search(self, query):
        tokenizer = Tokenizer()
        query_tokens = tokenizer.processItem(query)
        result = self.db.get_content_by_index(query_tokens)
        for r in result:
            for i in r:
                print(i)
        
class result(object):
    def __init__(self, url, title):
        self.url = url
        self.title = title
