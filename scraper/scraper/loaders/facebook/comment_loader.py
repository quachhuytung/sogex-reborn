import json

from scrapy.loader.processors import Compose, TakeFirst, Join, SelectJmes, Identity
from scrapy.loader import ItemLoader

from scraper.items.facebook import Comment

class CommentLoader(ItemLoader):
    default_item_class = Comment
    id_out = TakeFirst()
    content_out = Join()
    author_info_out = Identity()
    type_out = TakeFirst()
    post_id_out = TakeFirst()
    author_name_out = TakeFirst()
    author_url_out = TakeFirst()
