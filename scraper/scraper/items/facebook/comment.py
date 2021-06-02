import scrapy
from scrapy import Item

class Comment(Item):
    id = scrapy.Field()
    type = scrapy.Field()
    content = scrapy.Field()
    author_name = scrapy.Field()
    author_url = scrapy.Field()
    post_id = scrapy.Field()
