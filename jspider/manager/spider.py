# coding:utf-8
from __future__ import absolute_import, unicode_literals
from jspider.web.app import app_creator
from jspider.spider.base import BaseSpider
from jspider.utils import Config, lazy_load_module
import asyncio
from logging import getLogger
import os, sys, inspect
import importlib
import pkgutil

__author__ = "golden"
__date__ = '2018/6/2'


class SpiderManager(object):
    def __init__(self, loop=None, spider_path='spiders', home_path=None):
        self.loop = loop or asyncio.get_event_loop()
        self.logger = None
        self._spider_path = spider_path
        self.tasks = []
        self.home_path = home_path
        self.setup_logger()

    @staticmethod
    def add_spider(spider):
        asyncio.ensure_future(spider.tasks())

    def run_forever(self):
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
        if self.home_path:
            rel_path = self.home_path
        else:
            rel_path = os.path.abspath('.')
        spider_dir = os.path.join(rel_path, self._spider_path)
        return spider_dir

    def list_projects(self):
        spiders = []
        for _, package_name, _ in pkgutil.iter_modules([self.spider_path]):
            spiders.append(package_name)
        return spiders

    def list_spiders(self, cls=False):
        spiders = {}
        for importer, package_name, _ in pkgutil.iter_modules([self.spider_path]):
            spiders_file_or_path = os.path.join(self.spider_path, package_name, 'spiders.py')
            if os.path.exists(spiders_file_or_path):
                spec = importlib.util.spec_from_file_location(package_name,
                                                              '/root/golden/jspider/spiders/qb/spiders.py')
                module = spec.loader.load_module()
                for class_name, class_type in inspect.getmembers(module, inspect.isclass):
                    spider_class = getattr(module, class_name)
                    if spider_class.name and issubclass(spider_class, BaseSpider):
                        info = {'name': spider_class.name, 'doc': spider_class.__doc__}
                        if cls:
                            info['cls'] = spider_class
                        if package_name in spiders:
                            spiders[package_name].append(info)
                        else:
                            spiders[package_name] = [info]
        return spiders

    def load_spider(self, spider):  # spider name
        spiders = self.list_spiders(cls=True)
        for p in spiders:
            for sp in spiders[p]:
                if sp['name'] == spider:
                    return sp['cls']
        return None

    def setup_spider(self, spider, **kwargs):
        """
        setup a spider
        :param spider: name
        :return:
        """
        for importer, package_name, _ in pkgutil.iter_modules([self.spider_path]):
            spiders_file_or_path = os.path.join(self.spider_path, package_name, 'spiders.py')
            if os.path.exists(spiders_file_or_path):
                module = lazy_load_module(spiders_file_or_path)
                for class_name, class_type in inspect.getmembers(module, inspect.isclass):
                    spider_class = getattr(module, class_name)
                    if hasattr(spider_class, 'name') and spider_class.name == spider and issubclass(spider_class,
                                                                                                    BaseSpider):
                        return spider_class.setup_from_path(os.path.join(self.spider_path, package_name))
