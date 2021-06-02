import scrapy
from scrapy.shell import inspect_response
from scrapy.linkextractors import LinkExtractor

from . import FacebookCore
from scraper.config import config_data
from scraper.loaders.facebook import PostLoader
from scraper.utils.cookies import get_cookies


class FacebookProfileSpider(FacebookCore):
    name = 'facebook-profile'

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fanpage_url = kwargs['profile_url']
    
    @get_cookies
    def crawl_target(self, response):
        yield scrapy.Request(self.fanpage_url, callback=self.parse_meta_info)

    def parse_meta_info(self, response):
        profile_content_link_extractor = LinkExtractor(restrict_css=\
                config_data['facebook']['profile_page']['meta_info_page']['timeline_link_xpath'])
        timeline_link_containers = profile_content_link_extractor.extract_links(response)

        for timeline_link in timeline_link_containers:
            yield scrapy.Request(timeline_link.url, callback=self.crawl_timeline)

    def crawl_timeline(self, response):
        posts_link_container = LinkExtractor(restrict_xpaths=\
                config_data['facebook']['profile_page']['timeline_page']['post_link_xpath']).extract_links(response)
        for post_link in posts_link_container:
            yield scrapy.Request(post_link.url, callback=self.parse_post_content)

    def parse_post_content(self, response):
        post_loader = PostLoader(response=response)
        post_loader.add_xpath('content', config_data['facebook']['profile_page']['post_page']['contents_container_xpath'])
        post_loader.add_xpath('id', config_data['facebook']['profile_page']['post_page']['id_xpath'])

        yield post_loader.load_item()
