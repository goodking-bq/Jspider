#!/usr/bin/env python
# -*- coding:utf-8 -*-
from jspider.queue.base import BaseQueue
import asyncio

__author__ = 'golden'
__create_date__ = '2018/5/26 23:27'


class DefaultQueue(BaseQueue):
    def __init__(self, name, data_format='json', data_filter=None):
        super(DefaultQueue, self).__init__(name=name, data_format=data_format, data_filter=data_filter)
        self._queue = []  # asyncio.Queue()

    @classmethod
    def from_spider(cls, spider, name, data_format='json', data_filter=None):
        """
        :param spider: spider object
        :param data_format: data_format
        :param data_filter: data_filter
        :return:
        """
        return cls(name=name, data_format=data_format, data_filter=data_filter)

    async def push(self, request):
        self._queue.append(request)

    async def pop(self):
        if not await self.is_empty():
            return self._queue.pop()

    async def is_empty(self):
        return len(self._queue) == 0
