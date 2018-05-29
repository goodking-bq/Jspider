# coding:utf-8
from __future__ import absolute_import, unicode_literals
from logging import getLogger
import asyncio

__author__ = "golden"
__date__ = '2018/5/26'


class BaseDownloader(object):
    def __init__(self, spider):
        self.logger = None
        self.set_logger()
        self.spider = spider

    async def download(self, request, proxy=None, user_agent=None):
        raise NotImplementedError

    def set_logger(self):
        self.logger = getLogger(self.__class__.__name__)
        self.logger.debug("{name} setup success.".format(name=self.__class__.__name__))

    async def start(self):
        self.logger.debug('Downloader starting ...')
        while self.spider.doing():
            request = await self.spider.request_queue.pop()
            if not request:
                await asyncio.sleep(1)
            else:
                response = await self.download(request)
                await request.callback(response)
