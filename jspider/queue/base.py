#!/usr/bin/env python
# -*- coding:utf-8 -*-
import asyncio

__author__ = 'golden'
__create_date__ = '2018/5/26 23:20'


class BaseQueue(object):
    def __init__(self, spider):
        self.spider = spider

    async def push(self, request):
        raise NotImplementedError

    async def pop(self):
        raise NotImplementedError

    def is_empty(self):
        raise NotImplementedError
