import scrapy
from scrapy.shell import inspect_response

from scraper.config import config_data
from scraper.signals import log_cookie_signal, handle_log_cookie
from scraper.const.facebook import FACEBOOK_LOGIN_COOKIE
from scraper.utils.cookies import parse_cookies_to_dict

class FacebookCore(scrapy.Spider):
    name = 'facebook-core'
    allowed_domains = ['mbasic.facebook.com']
    start_urls = ['https://mbasic.facebook.com']

    def __init__(self, *args, **kwargs):
        ###             ARGUMENTS FROM COMMAND LINE             ###
        self.facebook_username = kwargs.get('username')
        self.facebook_password = kwargs.get('password')
        self.login_type = kwargs.get('login_type')
        self.cookie = kwargs.get('cookie')
        ###             END PARSING ARGUMENTS                   ###

        super(FacebookCore, self).__init__(*args, **kwargs)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(FacebookCore, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(handle_log_cookie, log_cookie_signal)
        return spider

    def start_requests(self):
        if self.login_type != FACEBOOK_LOGIN_COOKIE:
            for url in self.start_urls:
                yield scrapy.Request(url, callback=self.do_login)
        else:
            cookie_dict = parse_cookies_to_dict(self.cookie)
            for url in self.start_urls:
                yield scrapy.Request(url, cookies=cookie_dict, callback=self.crawl_target)


    
    def do_login(self, response):
        yield scrapy.FormRequest.from_response(response,
                formid=config_data['facebook']['login_page']['login_form_id'],
                formdata={
                    'email': self.facebook_username,
                    'pass': self.facebook_password
                }, 
                clickdata={
                    config_data['facebook']['login_page']['login_form_submit_button_attr']: \
                            config_data['facebook']['login_page']['login_form_submit_button_val']
                }, callback=self.after_login)
                

    def after_login(self, response):
        yield scrapy.FormRequest.from_response(response, 
                formxpath=config_data['facebook']['after_login_page']['save_login_form_xpath'],
                clickdata={
                    config_data['facebook']['after_login_page']['save_login_html_attr']: \
                        config_data['facebook']['after_login_page']['save_login_html_value']
                }, callback=self.crawl_target)

    def crawl_target(self, response):
        pass
