# coding:utf-8
from __future__ import absolute_import, unicode_literals
from logging import getLogger

__author__ = "golden"
__date__ = '2018/5/26'


class BaseDownloader(object):
    def __init__(self):
        self.logger = None
        self.set_logger()

    async def download(self, spider, url, proxy=None, user_agent=None):
        pass

    def set_logger(self):
        self.logger = getLogger(self.__class__.__name__)
        self.logger.debug("{name} setup success.".format(name=self.__class__.__name__))
