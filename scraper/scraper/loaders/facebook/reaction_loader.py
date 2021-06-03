import json

from scrapy.loader.processors import TakeFirst
from scrapy.loader import ItemLoader

from scraper.items.facebook import Reaction

class ReactionLoader(ItemLoader):
    default_item_class = Reaction
    obj_id_out = TakeFirst()
    obj_type_out = TakeFirst()
    stats_out = TakeFirst()
