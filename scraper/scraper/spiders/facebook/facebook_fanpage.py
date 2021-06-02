import scrapy
from scrapy.shell import inspect_response
from scrapy.linkextractors import LinkExtractor

from . import FacebookCore
from scraper.config import config_data
from scraper.loaders.facebook import PostLoader
from scraper.utils.facebook import get_cookies


class FacebookFanpageSpider(FacebookCore):
    name = 'facebook-fanpage'
    
    @get_cookies
    def crawl_target(self, response):
        yield scrapy.Request('https://mbasic.facebook.com/ChuyencuaHaNoi', callback=self.parse_meta_info)

    def parse_meta_info(self, response):
        fanpage_content_link_extractor = LinkExtractor(restrict_css=\
                config_data['facebook']['fanpage']['meta_info_page']['timeline_link_xpath'])
        timeline_link_containers = fanpage_content_link_extractor.extract_links(response)

        for timeline_link in timeline_link_containers:
            yield scrapy.Request(timeline_link.url, callback=self.crawl_timeline)

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
