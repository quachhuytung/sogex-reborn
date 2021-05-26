import scrapy


class FacebookFanpageSpider(scrapy.Spider):
    name = 'facebook-fanpage'
    allowed_domains = ['mbasic.facebook.com']
    start_urls = ['http://mbasic.facebook.com/']

    def parse(self, response):
        pass
