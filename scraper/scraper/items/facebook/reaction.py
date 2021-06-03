import scrapy
from scrapy import Item

class Reaction(Item):
    obj_id = scrapy.Field()
    obj_type = scrapy.Field()
    stats = scrapy.Field()
