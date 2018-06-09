# coding:utf-8
from __future__ import absolute_import, unicode_literals
from jspider.web.app import app
import asyncio
from logging import getLogger
import os, sys

__author__ = "golden"
__date__ = '2018/6/2'


class Manager(object):
    def __init__(self, loop=None, spider_path='./spiders'):
        self.web_app = app
        self.loop = loop or asyncio.get_event_loop()
        self.logger = None
        self._spider_path = spider_path

    @staticmethod
    def add_spider(spider):
        asyncio.ensure_future(spider.tasks())

    @classmethod
    def add_web(cls, host, port, debug):
        server = app.create_server(host=host, port=port, debug=debug)
        asyncio.ensure_future(server)

    def run(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt as e:
            print(asyncio.gather(*asyncio.Task.all_tasks()).cancel())
            self.loop.stop()
            self.loop.run_forever()
        finally:
            self.loop.close()
        self.logger.debug('stop success!')

    def setup_logger(self):
        self.logger = getLogger(self.__class__.__name__.lower())
        self.logger.debug("{name} setup success.".format(name=self.__class__.__name__))

    @property
    def spider_path(self):
        rel_path = os.path.dirname(sys.argv[0])
        spider_dir = os.path.join(rel_path, self._spider_path)
        return spider_dir

    def list_spiders(self):
        rel_path = os.path.dirname(sys.argv[0])
        spider_idr = os.path.join(rel_path, self.spider_path)
        spiders = []
        for p in os.listdir(spider_idr):
            if not os.path.isfile(p):
                spiders.append(p)
        return spiders

    def load_spider(self, spider):
        path = os.path.join(self.spider_path, spider)
