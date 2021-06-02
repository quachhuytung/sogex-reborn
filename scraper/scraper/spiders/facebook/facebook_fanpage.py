import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.shell import inspect_response

from . import FacebookCore
from scraper.config import config_data
from scraper.loaders.facebook import PostLoader
from scraper.utils.cookies import get_cookies


class FacebookProfileSpider(FacebookCore):
    name = 'facebook-fanpage'

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fanpage_url = kwargs['fanpage_url']
    
    @get_cookies
    def crawl_target(self, response):
        yield scrapy.Request(self.fanpage_url, callback=self.crawl_timeline)

    def crawl_timeline(self, response):
        posts_link_container = LinkExtractor(restrict_xpaths=\
                config_data['facebook']['fanpage']['timeline_page']['post_link_xpath']).extract_links(response)
        for post_link in posts_link_container:
            yield scrapy.Request(post_link.url, callback=self.parse_post_content)

    def parse_post_content(self, response):
        post_loader = PostLoader(response=response)
        post_loader.add_xpath('content', config_data['facebook']['fanpage']['post_page']['contents_container_xpath'])
        post_loader.add_xpath('id', config_data['facebook']['fanpage']['post_page']['id_xpath'])

        yield post_loader.load_item()
