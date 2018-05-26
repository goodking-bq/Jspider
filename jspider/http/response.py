#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'golden'
__create_date__ = '2018/5/26 22:38'


class Response(object):
    def __init__(self, url, body='', status=200, request=None):
        self.url = url
        self.body = body
        self.status = status
        self.request = request

    async def css(self):
        pass

    async def xpath(self):
        pass
