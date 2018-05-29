# coding:utf-8
from __future__ import absolute_import, unicode_literals
from jspider.spider.base import BaseSpider
from jspider.http.request import Request
import asyncio
from concurrent.futures import ProcessPoolExecutor

__author__ = "golden"
__date__ = '2018/5/26'


class Spider(BaseSpider):
    start_urls = ['http://www.baidu.com']
    name = 'spider'

    async def start_requests(self):
        for url in self.start_urls:
            await self.request_queue.push(await self.make_request(url))

    async def make_request(self, url):
        return Request(url, self.parse)

    async def run(self):
        self.logger.info("spider starting ....")
        await self.start_requests()
        asyncio.ensure_future(self.downloader.start())
        asyncio.ensure_future(self.pipe_line.start())
        self.logger.debug('starting success!')

        # for url in self.start_urls:
        #     # html = await self.downloader_cls().download(self, url)
        #     self.logger.debug(url)

    async def parse(self, response):
        await self.request_queue.push(await self.make_request('http://baidu.com'))
        await self.item_queue.push(dict(a=1))

    def doing(self):
        return True
