#!/usr/bin/env python
# -*- coding:utf-8 -*-
from pyquery import PyQuery
from urllib.parse import urljoin

__author__ = 'golden'
__create_date__ = '2018/5/26 22:38'


class Response(object):
    def __init__(self, url, body='', status=200, request=None):
        self.url = url
        self.body = body
        self.status = status
        self.request = request

    @classmethod
    def py_to_response(cls, index, element):
        return PyQuery(element)

    async def css(self, query):
        """"""
        py = PyQuery(self.body)
        py = py(query)
        return py.map(self.py_to_response)

    async def xpath(self):
        pass

    def url_join(self, url):
        return urljoin(self.url, url)
