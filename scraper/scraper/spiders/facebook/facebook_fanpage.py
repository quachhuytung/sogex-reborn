import scrapy
from scrapy.shell import inspect_response
from scrapy.linkextractors import LinkExtractor

from . import FacebookCore


class FacebookFanpageSpider(FacebookCore):
    name = 'facebook-fanpage'

    def crawl_target(self, response):
        yield scrapy.Request('https://mbasic.facebook.com/ChuyencuaHaNoi', callback=self.parse_meta_info)

    def parse_meta_info(self, response):
        fanpage_content_link_extractor = LinkExtractor(restrict_css='.basicNavItems.mfsm.fcg > a:first-child')
        timeline_link_containers = fanpage_content_link_extractor.extract_links(response)

        for timeline_link in timeline_link_containers:
            yield scrapy.Request(timeline_link.url, callback=self.crawl_timeline)

    def crawl_timeline(self, response):
        posts_link_container = LinkExtractor(restrict_xpaths='//div[@data-ft=\'{"tn":"*W"}\']/div[2]/a[1]').extract_links(response)
        for post_link in posts_link_container:
            yield scrapy.Request(post_link.url, callback=self.parse_post_content)

    def parse_post_content(self, response):
        post_content_paragraphs_container = response.xpath('//div[@data-ft=\'{"tn":"*s"}\']/div/p/text()')

        post_content = str()

        for paragraph in post_content_paragraphs_container:
            post_content = f'{post_content}{paragraph.get()}'

        print(post_content)
