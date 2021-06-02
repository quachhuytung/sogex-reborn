import scrapy
from scrapy import Item

class Post(Item):
    id = scrapy.Field()
    content = scrapy.Field()
