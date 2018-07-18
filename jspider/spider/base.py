# coding:utf-8
from __future__ import absolute_import, unicode_literals
from logging import getLogger
from jspider.utils import Loader, Config
import asyncio
from jspider.logger import setup_logger
import os, sys
from jspider.http import Request

__author__ = "golden"
__date__ = '2018/5/26'


class BaseState(object):
    def __init__(self):
        pass


class BaseSpider(object):
    start_urls = []
    name = ""
    setting = 'setting.py'

    def __init__(self, config=None, project_path=None, run_forever=False):
        self.logger = None
        self.project_path = project_path
        self.config = Config()
        self.config.update(config or {})
        self.request_queue = None
        self.item_queue = None
        self.downloader = None
        self.response_queue = None
        self.pipe_line = None
        self.run_forever = run_forever
        self.class_loader = None

    def setup_logger(self):
        setup_logger(os.path.dirname(os.path.abspath(__file__)), 'main')
        self.logger = getLogger(self.__class__.__name__.lower())
        self.logger.debug("{name} setup success.".format(name=self.__class__.__name__))

    def setup_spider(self):
        self.request_queue = self.class_loader(self.config.get('REQUEST_QUEUE_CLS')).from_spider(
            self,
            name='request',
            data_format='pickle',
            data_filter=True)
        self.item_queue = self.class_loader(self.config.get('QUEUE_CLS')).from_spider(self,
                                                                                      'item')
        self.response_queue = self.class_loader(self.config.get('QUEUE_CLS')).from_spider(self,
                                                                                          'response')
        self.downloader = self.class_loader(self.config.get('DOWNLOADER_CLS'))(self)
        self.pipe_line = self.class_loader(self.config.get('PIPE_LINE_CLS')).from_spider(self)
        self.setup_logger()

    @classmethod
    def setup_from_path(cls, path):  # setting is a py module
        spider = cls(project_path=path)
        loader = Loader(from_path=path)
        spider.class_loader = loader.lazy_load_class
        setting_obj = loader.lazy_load_module('config')
        spider.config.from_object(setting_obj)
        spider.setup_spider()
        return spider

    async def start_requests(self):
        for url in self.start_urls:
            await self.make_request(url)

    async def parse(self, response):
        raise NotImplementedError

    async def make_request(self, url):
        await self.request_queue.push(Request(url, 'parse'))

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(self.start_requests()))
        # asyncio.ensure_future(self.start_requests())
        asyncio.ensure_future(self.pipe_line.start())
        asyncio.ensure_future(self.downloader.start())
        asyncio.ensure_future(self._check_done(loop))
        self.logger.debug('spider starting success!')
        try:
            loop.run_forever()
        except KeyboardInterrupt as e:
            print(asyncio.gather(*asyncio.Task.all_tasks()).cancel())
            loop.stop()
            loop.run_forever()
        finally:
            loop.close()
        self.logger.debug('stop success!')

    async def doing(self):
        """
        """
        return self.run_forever or not (
                await self.item_queue.is_empty() and await self.response_queue.is_empty() and await self.request_queue.is_empty())

    def done(self):
        return self.downloader.has_done and self.pipe_line.has_done

    async def _check_done(self, loop):
        while not self.done():
            await asyncio.sleep(0.1)
        asyncio.gather(*asyncio.Task.all_tasks()).cancel()
        loop.stop()

    async def tasks(self):
        self.logger.info("spider starting ....")
        asyncio.ensure_future(self.start_requests())
        asyncio.ensure_future(self.pipe_line.start())
        asyncio.ensure_future(self.downloader.start())
        self.logger.debug('starting success!')
