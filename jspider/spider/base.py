# coding:utf-8
from __future__ import absolute_import, unicode_literals
from logging import getLogger
from jspider.utils.loader import load_class
import asyncio
from jspider.logger import setup_logger
import os
from jspider.http import Request

__author__ = "golden"
__date__ = '2018/5/26'


class BaseSpider(object):
    start_urls = []

    def __init__(self, downloader_cls='jspider.downloader.AioHttpDownloader', queue_cls='jspider.queue.DefaultQueue',
                 pipe_line_cls='jspider.pipeline.ConsolePipeLine'):
        self.name = ''
        self.logger = None
        self.downloader_cls = load_class(downloader_cls)
        self.queue_cls = load_class(queue_cls)
        self.pipe_line_cls = load_class(pipe_line_cls)
        self.request_queue = None
        self.item_queue = None
        self.downloader = None
        self.response_queue = None
        self.pipe_line = None
        self.setup_spider()

    def setup_logger(self):
        setup_logger(os.path.dirname(os.path.abspath(__file__)), 'main')
        self.logger = getLogger(self.__class__.__name__.lower())
        self.logger.debug("{name} setup success.".format(name=self.__class__.__name__))

    def setup_spider(self):
        self.request_queue = self.queue_cls(self)
        self.item_queue = self.queue_cls(self)
        self.response_queue = self.queue_cls(self)
        self.downloader = self.downloader_cls(self)
        self.pipe_line = self.pipe_line_cls(self)
        self.setup_logger()

    async def start_requests(self):
        for url in self.start_urls:
            await self.make_request(url)

    async def parse(self, response):
        raise NotImplementedError

    async def make_request(self, url):
        await self.request_queue.push(Request(url, self.parse))

    def run(self):
        self.logger.info("spider starting ....")
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.start_requests())
        asyncio.ensure_future(self.pipe_line.start())
        asyncio.ensure_future(self.downloader.start())
        asyncio.ensure_future(self._check_done(loop))
        self.logger.debug('starting success!')
        try:
            loop.run_forever()
        except KeyboardInterrupt as e:
            print(asyncio.gather(*asyncio.Task.all_tasks()).cancel())
            loop.stop()
            loop.run_forever()
        finally:
            loop.close()
        self.logger.debug('stop success!')

    def doing(self):
        return not (self.item_queue.is_empty() and self.response_queue.is_empty() and self.request_queue.is_empty())

    def done(self):
        return self.downloader.has_done and self.pipe_line.has_done

    async def _check_done(self, loop):
        while not self.done():
            await asyncio.sleep(0.1)
        asyncio.gather(*asyncio.Task.all_tasks()).cancel()
        loop.stop()
