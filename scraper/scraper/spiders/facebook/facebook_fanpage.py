import scrapy

from . import FacebookCore


class FacebookFanpageSpider(FacebookCore):
    name = 'facebook-fanpage'
