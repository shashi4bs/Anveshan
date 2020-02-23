from scrapy import Item, Field

class Article(Item):
    url =  Field()
    title = Field()
    content = Field()
    lastUpdated = Field()
    links = Field()

