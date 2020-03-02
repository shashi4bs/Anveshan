from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from AnveshanCrawler.items import Article

class ArticleSpider(CrawlSpider):
    '''
        extends parent scrapy.Spider
        overwrite parse_items method to perform scraping.
        Article -> represent a page on the website with url, title, content and lastUpdate
    '''
    
    name = 'articleSpider'
    allowed_domains = ['wikipedia.org']
    #start_urls = ["https://en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Tourism"]
    rules = [
        #internalLinks
        Rule(LinkExtractor(allow='(en.wikipedia.org/wiki/)((?!:).)*$'), callback='parse_items', follow=True, cb_kwargs={'parse': True}),
        #externalLinks
        #Rule(LinkExtractor(allow=r'.*'), callback='parse_items', follow=True, cb_kwargs={'parse': False})
    ]

    def parse_items(self, response, parse):
        if(parse):
            #print(response.url)
            article = Article()
            article['url'] = response.url
            article['title'] = response.xpath('//h1//text()').extract()
            article['content'] = response.xpath('//div[@id="mw-content-text"]')
            article['content'] = article['content'].xpath('//div[@class="mw-parser-output"]//p//text()').extract()
            article['links'] = response.xpath('//a[contains(@href, "/wiki/")]/@href').extract()
            #print(article['links'])
            #print(article['content'])
            yield article 
