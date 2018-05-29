# coding:utf-8
from __future__ import absolute_import, unicode_literals
from logging import getLogger
from jspider.utils.loader import load_class
import asyncio
from jspider.logger import setup_logger
import os

__author__ = "golden"
__date__ = '2018/5/26'


class BaseSpider(object):
    def __init__(self, downloader_cls, queue_cls='jspider.queue.DefaultQueue',
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
        raise NotImplementedError

    def run(self):
        self.logger.info("spider starting ....")
        asyncio.ensure_future(self.start_requests())

        asyncio.ensure_future(self.pipe_line.start())
        asyncio.ensure_future(self.downloader.start())
        self.logger.debug('starting success!')
        loop = asyncio.get_event_loop()
        try:
            loop.run_forever()
        except KeyboardInterrupt as e:
            print(asyncio.gather(*asyncio.Task.all_tasks()).cancel())
            loop.stop()
            loop.run_forever()
        finally:
            loop.close()
