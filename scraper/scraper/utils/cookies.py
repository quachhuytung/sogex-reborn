import functools

from scraper.signals import log_cookie_signal
from scraper.const.facebook import FACEBOOK_LOGIN_COOKIE

def get_cookies(f):
    @functools.wraps(f)
    def log_cookies(*args, **kwargs):
        spider, response = args
        cookies = response.request.headers['Cookie'].decode('utf-8')

        if spider.login_type != FACEBOOK_LOGIN_COOKIE:
            spider.crawler.signals.send_catch_log(log_cookie_signal, cookies=cookies)
            spider.logger.info('Logged Cookie')

        result = f(*args, **kwargs)
        return result
    return log_cookies

def parse_cookies_to_dict(cookie_str):
    cookie_k_v = cookie_str.split(';')
    cookie_k_v = list(map(lambda x: x.strip(), cookie_k_v))
    return {
        element.split('=')[0]:element.split('=')[1] for element in cookie_k_v
    }

