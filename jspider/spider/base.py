# coding:utf-8
from __future__ import absolute_import, unicode_literals
from logging import getLogger

__author__ = "golden"
__date__ = '2018/5/26'


class BaseSpider(object):
    def __init__(self, downloader):
        self.name = ''
        self.logger = None
        self.downloader = downloader()

        self.set_logger()

    def set_logger(self):
        self.logger = getLogger(self.__class__.__name__.lower())
        self.logger.debug("{name} setup success.".format(name=self.__class__.__name__))

    async def run(self):
        pass
