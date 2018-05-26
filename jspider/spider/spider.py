# coding:utf-8
from __future__ import absolute_import, unicode_literals
from jspider.spider.base import BaseSpider
from jspider.http.request import Request

__author__ = "golden"
__date__ = '2018/5/26'


class Spider(BaseSpider):
    start_urls = ['http://www.baidu.com']
    name = 'spider'

    async def start_requests(self):
        for url in self.start_urls:
            self.queue.push(await self.make_request(url))

    async def make_request(self, url):
        return Request(url, self.parse)

    async def run(self):
        self.logger.info("spider starting ....")
        self.queue = self.queue_class(self)
        self.start_requests()
        while self.doing():
            pass
        for url in self.start_urls:
            html = await self.downloader.download(self, url)
            self.logger.debug(html)

    async def parse(self, response):
        pass

    def doing(self):
        return not self.queue.is_empty()
