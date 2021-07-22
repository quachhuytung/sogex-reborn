import json

from scrapy.loader.processors import Compose, TakeFirst, Join, SelectJmes, Identity
from scrapy.loader import ItemLoader

from scraper.items.facebook import Comment

import re
pattern = pattern = re.compile("\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*")

def get_email(value):
    match = pattern.search(value)
    if match:
        return match.group(0)
    else:
        return 'NOT FOUND'

def add_fb_domain(value):
    return 'facebook.com' + value

class CommentLoader(ItemLoader):
    default_item_class = Comment
    id_out = TakeFirst()
    content_out = Join('')
    author_info_out = Identity()
    type_out = TakeFirst()
    post_id_out = TakeFirst()
    author_name_out = TakeFirst()
    author_url_out = Compose(TakeFirst(), add_fb_domain)
    email_out = Compose(Join(''), get_email)
