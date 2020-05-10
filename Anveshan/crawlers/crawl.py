import re
from utils.async_utils import run_in_parallel
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

#import all crawlers
from crawlers.wikipedia_crawler import getWikipediaSpider 

def run_spider(spider):
	try:
		process = CrawlerRunner()
		process.crawl(spider) 
		reactor.run()
	except Exception as e:
		print(e)


def get_pages(response, query):
	for r in response:
		spider = None
		#search for respective crawler
		if(re.search(".*wikipedia.*", r["url"])):
			spider = getWikipediaSpider(r["url"], query, r["_id"])
			
		if(spider):
			run_in_parallel(run_spider, spider)
			#run_spider.apply_async(args=[spider,])
