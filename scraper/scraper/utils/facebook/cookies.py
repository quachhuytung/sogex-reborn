import functools

from scraper.signals import log_cookie_signal

def get_cookies(f):
    @functools.wraps(f)
    def log_cookies(*args, **kwargs):
        spider, response = args
        cookies = response.request.headers['Cookie'].decode('utf-8')
        spider.crawler.signals.send_catch_log(log_cookie_signal, cookies=cookies)
        spider.logger.info('Logged Cookie')
        result = f(*args, **kwargs)
        return result
    return log_cookies
