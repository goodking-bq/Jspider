#!/usr/bin/env python
# -*- coding:utf-8 -*-
from logging import getLogger

__author__ = 'golden'
__create_date__ = '2018/5/26 22:23'


class Request(object):
    def __init__(self, url, callback):
        self.url = url
        self.callback = callback
        self.logger = None

    def set_logger(self):
        self.logger = getLogger(self.__class__.__name__)
        self.logger.debug("{name} setup success.".format(name=self.__class__.__name__))

    def __str__(self):
        return self.url
