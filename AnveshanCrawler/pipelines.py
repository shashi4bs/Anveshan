#from AnveshanCrawler.items import Article
import os
import sys
from constants import DIR
sys.path.append(os.path.abspath(DIR))

from scrapy.exceptions import DropItem
import pymongo
from text_normalizer import Tokenizer
from mongo.mongodump import MongoPipeline
from Tagger.generator import TagGenerator


db = MongoPipeline()
tagger = TagGenerator()

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
        print('Spider Name: ', spider)
        #item['content'] -> list of text contents.
        content = "".join(item['content'])
        item['tags'] = tagger.generate_tag(content)
        tokenizedContent = processContent(content)
        item['content'] = tokenizedContent.filtered_tokens
        #print(processContent(item['title']))
        
        #db.save(item) ##store tokenizedContent and title in form of inverted index
        return item
