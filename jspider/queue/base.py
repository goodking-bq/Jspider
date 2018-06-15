#!/usr/bin/env python
# -*- coding:utf-8 -*-
import asyncio
import json
import pickle

__author__ = 'golden'
__create_date__ = '2018/5/26 23:20'


class BaseQueue(object):
    def __init__(self, name, data_format='json', data_filter=None):
        """
        :param data_format:
        :param data_filter:
        """
        self.data_format = data_format
        self.data_filter = data_filter
        self.name = name

    @classmethod
    def from_spider(cls, spider, name, data_format='json', data_filter=None):
        raise NotImplementedError

    async def push(self, item):
        raise NotImplementedError

    async def pop(self):
        raise NotImplementedError

    async def is_empty(self):
        raise NotImplementedError

    def dumps(self, item):
        if self.data_format == 'json':
            data = json.dumps(item)
        elif self.data_format == 'pickle':
            data = pickle.dumps(item)
        else:
            data = item
        return data

    def loads(self, item):
        if self.data_format == 'json':
            data = json.loads(item)
        elif self.data_format == 'pickle':
            data = pickle.loads(item)
        else:
            data = item
        return data
