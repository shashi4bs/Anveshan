import scrapy
from crawlers.page import Page
from crawlers.helper import filter_text_from_content
from app import socketio
import logging
from config import LOG, LOG_LEVEL
import traceback



def getWikipediaSpider(url, query, content_id):
       
    class wikipedia(scrapy.Spider):
        name="wikipedia"    
        allowed_domains = ["wikipedia.org"]
        start_urls=[url]

        def __init__(self):
            scrapy.utils.log.configure_logging({
                'LOG_ENABLED' : LOG,
                'LOG_LEVEL' : LOG_LEVEL
            })

        def parse(self, response):
            print("parsing")
            page = Page()
            page['url'] = response.url
            page['content'] = response.xpath('//div[@id="mw-content-text"]')
            page['content'] = page['content'].xpath('//div[@class="mw-parser-output"]//p//text()').extract()
            #filter content
            text_to_send = filter_text_from_content(page, query)
            #print(text_to_send)
            try:
                print("socket")
                socketio.emit("content", {'data': text_to_send, "_id": content_id}, broadcast=True)
                print("socket emit")
            except Exception as e:
                traceback.print_exc()
                print("Exception", e)
    return wikipedia
