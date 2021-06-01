import scrapy
from scrapy.shell import inspect_response


from scraper.config import config_data


class FacebookCore(scrapy.Spider):
    name = 'facebook-core'
    allowed_domains = ['mbasic.facebook.com']
    start_urls = ['https://mbasic.facebook.com']

    def __init__(self, *args, **kwargs):
        ###             ARGUMENTS FROM COMMAND LINE             ###
        self.facebook_username = kwargs.get('username')
        self.facebook_password = kwargs.get('password')
        ###             END PARSING ARGUMENTS                   ###

        super(FacebookCore, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.do_login)

    
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
