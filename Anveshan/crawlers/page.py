from scrapy import Item, Field

class Page(Item):
	url = Field()
	content = Field()
	last_updated = Field()
