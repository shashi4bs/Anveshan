import scrapy
from scrapy.crawler import CrawlerProcess
from helper import processBody
from mongo.contributions import UserContrib

usercontribDB = UserContrib()

def getGeneralCrawler(url, username)
    class Crawler(scrapy.Spider):
        name = "trump spider"
        start_urls=[url]

        def __init__(self):
            self.username = username
            scrapy.utils.log.configure_logging({
                'LOG_ENABLED': False,
                'LOG_STDOUT' : True
                })
        def parse(self, response):
            #print("Resposne : ", response)
            #print("URL : ", response.url)
            #print("Body : ", response.body)
            content = processBody(response.body)
            usercontribDB.save_content(content, url, username)
       
    return Crawler

#process = CrawlerProcess()
#process.crawl(Crawler)
#process.start()
