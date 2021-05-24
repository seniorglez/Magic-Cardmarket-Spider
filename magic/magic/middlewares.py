# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
import random
import logging

from stem import Signal
from stem.control import Controller

from magic import settings

import scrapy
from scrapy.crawler import Crawler
from scrapy.settings import BaseSettings
from scrapy.spiders import Spider
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

class MagicSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class MagicDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class RandomUserAgentMiddleware:

    def process_request(self, request, spider):
        ua  = random.choice(settings.USER_AGENT_LIST) # good enough for now
        if ua:
            request.headers.setdefault('User-Agent', ua)

class TorProxyMiddleware:

    logger = logging.getLogger("tor-proxy-middleware")
    enabled = False
    proxy_url ="http://localhost:8118"
    control_password = ""

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        try:
            spider_attr = getattr(spider, "TOR_PROXY_ENABLED")
        except AttributeError:
            if not spider.crawler.settings.getbool("TOR_PROXY_ENABLED"):
                self.enabled = False
                self.logger.info("Tor Proxy disabled (TOR_PROXY_ENABLED setting)")
                return
        else:
            if not BaseSettings({"enabled": spider_attr}).getbool("enabled"):
                self.enabled = False
                self.logger.info("Tor Proxy disabled (tor_proxy_enabled spider attribute)")
                return
            
        self.enabled = True
        self._read_settings(spider.crawler.settings)
        if self.enabled:
            self.logger.info("Using Tor Proxy at %s", self.proxy_url)
     
    def _read_settings(self, settings):
        if not settings.get("TOR_PROXY_CONTROL_PASSWORD"):
            self.enabled = False
            self.logger.info("Tor Proxy cannot be used without a control password")
            return
        
        self.control_password = settings["TOR_PROXY_CONTROL_PASSWORD"]

    def process_request(self, request, spider):
        if not self.enabled:
            return None
        request.meta['proxy'] = self.proxy_url
        self.set_new_ip()
    
    def set_new_ip(self):
        """Change IP using TOR"""
        with Controller.from_port(port=9051) as controller:
            if controller.is_newnym_available():
                try:
                    controller.authenticate(self.control_password)
                    controller.signal(Signal.NEWNYM)
                except:
                    print("Unable to authenticate, password is incorrect")
            else:
                print("No newnym available")