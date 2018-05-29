# coding:utf-8
from __future__ import absolute_import, unicode_literals
from .base import BasePipeLine

__author__ = "golden"
__date__ = '2018/5/29'


class ConsolePipeLine(BasePipeLine):
    async def process_item(self, item):
        self.logger.info(item)
