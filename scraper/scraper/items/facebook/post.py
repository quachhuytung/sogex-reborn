import scrapy
from scrapy import Item

class Post(Item):
    id = scrapy.Field()
    content = scrapy.Field()
    type = scrapy.Field()
    author_name = scrapy.Field()
    author_url = scrapy.Field()
