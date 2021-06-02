import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.shell import inspect_response

from . import FacebookCore
from scraper.config import config_data
from scraper.loaders.facebook import PostLoader, CommentLoader
from scraper.utils.cookies import get_cookies


class FacebookProfileSpider(FacebookCore):
    name = 'facebook-fanpage'

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fanpage_url = kwargs['fanpage_url']
        self.max_scroll_timeline = int(kwargs['max_scroll_timeline'])
        self.max_scroll_comment = int(kwargs['max_scroll_comment'])
    
    @get_cookies
    def crawl_target(self, response):
        yield scrapy.Request(self.fanpage_url, callback=self.crawl_timeline, 
                cb_kwargs={
                    'timeline_n_times': 1
                }
            )

    def crawl_timeline(self, response, timeline_n_times):
        posts_link_container = LinkExtractor(restrict_xpaths=\
                config_data['facebook']['fanpage']['timeline_page']['post_link_xpath']).extract_links(response)
        for post_link in posts_link_container:
            yield scrapy.Request(post_link.url, callback=self.parse_post_content,
                    cb_kwargs = {
                        'comment_list_n_times' : 1
                    })
        if timeline_n_times < self.max_scroll_timeline:
            more_posts_link_container = LinkExtractor(restrict_text=\
                config_data['facebook']['fanpage']['timeline_page']['more_post_restrict_text'])\
                    .extract_links(response)
            if more_posts_link_container:
                yield scrapy.Request(more_posts_link_container[0].url, callback=self.crawl_timeline, cb_kwargs={
                        'timeline_n_times': timeline_n_times + 1
                    }
                )

    def parse_post_content(self, response, comment_list_n_times):
        post_loader = PostLoader(response=response)
        post_loader.add_xpath('content', config_data['facebook']['fanpage']['post_page']['contents_container_xpath'])
        post_loader.add_xpath('id', config_data['facebook']['fanpage']['post_page']['id_xpath'])
        post_loader.add_value('type', 'post')

        if comment_list_n_times == 1: # first time visit this page
            yield post_loader.load_item()

        post_id = post_loader.get_output_value('id')
        comments_container = response.xpath(config_data['facebook']['fanpage']['post_page']['comment_container_dynamic_xpath'], 
                postIdContainer=f'ufi_{post_id}')

        if comment_list_n_times < self.max_scroll_comment:
            next_comment_page_url_container = LinkExtractor(\
                restrict_xpaths=config_data['facebook']['fanpage']['post_page']['next_comment_page_dynamic_xpath']\
                    .format(post_id=post_id)).extract_links(response)

            if next_comment_page_url_container:
                yield scrapy.Request(next_comment_page_url_container[0].url, callback=self.parse_post_content, 
                        cb_kwargs = {
                            'comment_list_n_times' : comment_list_n_times + 1
                        }
                )

        for comment_container in comments_container[:-1]: # last one is for next page
            comment_loader = CommentLoader(response=response)
            comment_loader.add_value('id', comment_container.xpath(\
                config_data['facebook']['fanpage']['post_page']['comment_id_relative_xpath']).get())
            comment_loader.add_value('content', comment_container.xpath(\
                config_data['facebook']['fanpage']['post_page']['comment_content_relative_xpath'])\
                    .getall())
            comment_loader.add_value('post_id', post_id)
            comment_loader.add_value('type', 'comment')
            comment_loader.add_value('author_name', \
                comment_container.xpath(config_data['facebook']['fanpage']['post_page']['comment_author_name_relative_xpath']).get())
            comment_loader.add_value('author_url', \
                comment_container.xpath(config_data['facebook']['fanpage']['post_page']['comment_author_url_relative_xpath']).get())
            yield comment_loader.load_item()
