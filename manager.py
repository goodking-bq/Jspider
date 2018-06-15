# coding:utf-8
from __future__ import absolute_import, unicode_literals
from jspider.manager import Manager

__author__ = "golden"
__date__ = '2018/6/4'
if __name__ == '__main__':
    manager = Manager()
    spider = manager.setup_spider('qb')
    manager.add_spider(spider)
    manager.run_forever()
