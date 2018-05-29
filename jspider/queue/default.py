#!/usr/bin/env python
# -*- coding:utf-8 -*-
from jspider.queue.base import BaseQueue
import asyncio

__author__ = 'golden'
__create_date__ = '2018/5/26 23:27'


class DefaultQueue(BaseQueue):
    def __init__(self, spider):
        super(DefaultQueue, self).__init__(spider)
        self._queue = []  # asyncio.Queue()

    async def push(self, request):
        self._queue.append(request)

    async def pop(self):
        if not self.is_empty():
            return self._queue.pop()

    def is_empty(self):
        return len(self._queue) == 0
