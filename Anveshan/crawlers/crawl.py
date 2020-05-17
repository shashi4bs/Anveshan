import re
from utils.async_utils import run_in_parallel, run_process, run_spiders_in_parallel
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from twisted.internet import reactor
from flask_login import current_user
import traceback

#import all crawlers
from crawlers.wikipedia_crawler import getWikipediaSpider 

def run_spider(spider):
	try:
		print("start Spider")
		#process = CrawlerRunner()
		process = CrawlerProcess()
		process.crawl(spider)
		process.start()
		#if reactor.running:
		#reactor.stop()
		#run_in_parallel(reactor.run, False)
	except Exception as e:
		traceback.print_exc()
		print("Exception", e)


def get_pages(response, query):
	for r in response:
		spider = None
		#search for respective crawler
		if(re.search(".*wikipedia.*", r["url"])):
			spider = getWikipediaSpider(r["url"], query, r["_id"])
			
		if(spider):
			if current_user:
				thread_name = current_user.username
			else:
				thread_name = "default"
			#run_spiders_in_parallel(True, thread_name, run_spider, spider)
			run_process(run_spider, spider)
			#run_spider.apply_async(args=[spider,])

	try:
		print("test")
	except Exception as e:
		traceback.print_exc()
		print("Exception", e)
