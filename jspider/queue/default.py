#!/usr/bin/env python
# -*- coding:utf-8 -*-
from jspider.queue.base import BaseQueue
import asyncio

__author__ = 'golden'
__create_date__ = '2018/5/26 23:27'


class DefaultQueue(BaseQueue):
    def __init__(self, spider):
        super(DefaultQueue, self).__init__(spider)
        self._queue = asyncio.Queue()

    async def push(self, request):
        self._queue.put_nowait(request)

    async def pop(self):
        self._queue.get_nowait()

    def is_empty(self):
        return self._queue.empty()
