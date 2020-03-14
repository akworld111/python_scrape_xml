from scrapy import signals
import random
from scrapy.core.downloader.handlers.http11 import TunnelError
import gzip
import logging
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
import time
import socket
from scrapy.exceptions import DontCloseSpider




class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = spider.crawler.settings.get('HTTP_PROXY')
        # proxy_user_pass = "helle1:dfhd234sdf"
        # encoded_user_pass = base64.encodestring(proxy_user_pass).replace('\n', '')
        # headers = {'Proxy-Authorization': 'Basic ' + encoded_user_pass}

# class ForceUTF8Response(object):
#     """A downloader middleware to force UTF-8 encoding for all responses."""
#     encoding = 'utf-8'

#     def process_response(self, request, response, spider):
#         # Note: Use response.body_as_unicode() instead of response.text in in Scrapy <1.0.
#         return response.replace(encoding='UTF-8')
        

class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = random.choice(spider.crawler.settings.get('USER_AGENT_LIST'))
        if ua:
            request.headers.setdefault('User-Agent', ua)




class MySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_idle, signal=signals.spider_idle)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s
    
    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.
        
        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        # if ( isinstance(exception, self.EXCEPTIONS_TO_RETRY) or isinstance(exception, TunnelError) ) \
        #         and 'dont_retry' not in request.meta:
        #     print("=========== hehehe")
        #     print (response.status)
        #     return self._retry(request, exception, spider)

        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesnt have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def spider_idle(self, spider):
        spider.logger.info('===> Spider idle: %s.' % spider.name)
        
        # spider.logger.info('I am alive. Request more data...')
        # # spider.crawler.engine.crawl(spider.create_more_requests(), spider)
        # reqs = spider.start_requests()
        # if not reqs:
        #     return
        # for req in reqs:
        #     spider.crawler.engine.schedule(req, spider)
        # raise DontCloseSpider

    
    def spider_closed(self, spider):
        # second param is instance of spder about to be closed.
        spider.logger.info('Spider {} closed at {}'.format(spider.name, time.strftime('%Y-%m-%d %H:%M:%S')))

        if spider.crawler.settings.get('IS_STOP_REPORT'):
            msg = 'Spider: {} on machine:{} stopp... at: {}'.format(spider.name, socket.gethostname(), time.strftime('%Y-%m-%d %H:%M:%S'))
            # notifyEmail('{} notify'.format(spider.name), msg, 'etuannv@gmail.com')

    


    

