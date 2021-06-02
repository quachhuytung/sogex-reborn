import scrapy
from scrapy import Item

class User(Item):
    id = scrapy.Field()
    name = scrapy.Field()
    profile_url = scrapy.Field()
    type = scrapy.Field()
