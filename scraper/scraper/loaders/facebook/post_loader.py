import json

from scrapy.loader.processors import Compose, TakeFirst, Join, SelectJmes
from scrapy.loader import ItemLoader

from scraper.items.facebook import Post

class PostLoader(ItemLoader):
    default_item_class = Post
    id_out = Compose(TakeFirst(), json.loads, SelectJmes('mf_story_key'))
    content_out = Join()
    type_out = TakeFirst()
