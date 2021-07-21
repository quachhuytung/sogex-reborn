import json

from scrapy.loader.processors import Compose, TakeFirst, Join, SelectJmes
from scrapy.loader import ItemLoader

from scraper.items.facebook import Post

def get_post_id(value, loader_context):
    scrape_type = loader_context['scrape_type']
    if (scrape_type == 'group'):
        return value['top_level_post_id']
    else:
        return value['mf_story_key']

class PostLoader(ItemLoader):
    default_item_class = Post
    id_out = Compose(TakeFirst(), json.loads, get_post_id)
    content_out = Join()
    type_out = TakeFirst()
    author_name_out = TakeFirst()
    author_url_out = TakeFirst()
