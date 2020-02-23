#from AnveshanCrawler.items import Article
import os
import sys
from contants import DIR
sys.path.append(os.path.abspath(DIR))

from scrapy.exceptions import DropItem
import pymongo
from text_normalizer import Tokenizer
from mongodump import MongoPipeline



db = MongoPipeline()

def processContent(content):
    '''
     input - content as string
     -> tokenize text
    '''
    tokenizer = Tokenizer()
    tokens = tokenizer.processItem(content, removeStopWords=True) 
    #print(tokens)
    return tokenizer

class AnveshancrawlerPipeline(object):

    def process_item(self, item, spider):
        #item['content'] -> list of text contents.
        content = "".join(item['content'])
        tokenizedContent = processContent(content)
        item['content'] = tokenizedContent.filtered_tokens
        #print(processContent(item['title']))
        db.save(item) ##store tokenizedContent and title in form of inverted index
        return item
