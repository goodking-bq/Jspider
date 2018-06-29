# coding:utf-8
from __future__ import absolute_import, unicode_literals

__author__ = "golden"
__date__ = '2018/6/29'

from jspider.web.app import app_creator

app = app_creator()
if __name__ == '__main__':
    app.run()
