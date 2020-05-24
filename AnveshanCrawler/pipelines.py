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
from helper import make_full_links, make_content_matrix

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
        base_url = "https://en.wikipedia.org"
        print('Spider Name: ', spider)

        #item['content'] -> list of text contents.
        content = "".join(item['content'])
        item['tags'] = tagger.generate_tag(content)
        #tag processing-> remove it from here later
        item['tags'] = item['tags'].replace('\n', '')
        item['tags'] = item['tags'].lower()
        item['links'] = make_full_links(item['links'], base_url)
        tokenizedContent = processContent(content)
        item['content'] = tokenizedContent.filtered_tokens
        print(item['content'])
        #prepare content matrix
        item['content_matrix'] = make_content_matrix(item['content'])
        #print("Item Content", item['content'])
        db.save(item) ##store tokenizedContent and title in form of inverted index
        return item
