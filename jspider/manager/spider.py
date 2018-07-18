# coding:utf-8
from __future__ import absolute_import, unicode_literals
from jspider.web.app import app_creator
from jspider.spider.base import BaseSpider
from jspider.utils import Loader
import asyncio
from logging import getLogger
import os, sys, inspect, zipfile, zipimport
import importlib
import pkgutil

__author__ = "golden"
__date__ = '2018/6/2'


class _Manager(object):
    def __init__(self, path, parent_path, logger=None):
        self.logger = logger
        self.path = path
        self.parent_path = parent_path
        self.full_path = os.path.join(parent_path, path)
        if not os.path.exists(self.full_path):
            os.mkdir(self.full_path)

    def projects(self, cls=False):
        raise NotImplementedError

    def spiders(self, project, cls=False):
        raise NotImplementedError

    def load_project(self, project):
        raise NotImplementedError

    def load_spider(self, project, spider):
        raise NotImplementedError


class _Source(_Manager):
    def __init__(self, parent_path, logger=None):
        super(_Source, self).__init__('sources', parent_path, logger)

    def projects(self, cls=False):
        projects = []
        for _, package_name, _ in pkgutil.iter_modules([self.full_path]):
            project = os.path.join(self.full_path, package_name, '__init__.py')
            if not os.path.exists(project):
                self.logger.debug("%s is not a package, had passed." % project)
                continue
            module = Loader(self.full_path).lazy_load_module(package_name)
            _project = {'package': package_name, 'name': module.__name__, 'author': module.__author__,
                        'create_date': module.__date__, 'description': module.__description__,
                        'version': module.__version__, 'spiders': self.spiders(package_name, cls),
                        'doc': module.__doc__, 'from': 'source', 'path': os.path.join(self.full_path, package_name)}
            projects.append(_project)
        return projects

    def spiders(self, project, cls=False):
        _spiders = []
        p = os.path.join(self.full_path, project)
        module = Loader(p).lazy_load_module('spiders')
        for class_name, class_type in inspect.getmembers(module, inspect.isclass):
            spider_class = getattr(module, class_name)
            if spider_class.name and issubclass(spider_class, BaseSpider):
                info = {'name': spider_class.name, 'doc': spider_class.__doc__, 'project_path': p}
                if cls:
                    info['cls'] = spider_class
                _spiders.append(info)
        return _spiders

    def zip(self, project):
        output = os.path.join(self.full_path, '../zips')
        if not os.path.exists(output):
            os.mkdir(output)
        output = os.path.join(output, '%s.zip' % project)
        source = os.path.join(self.full_path, project)
        zf = zipfile.ZipFile(output, 'w')
        pre_len = len(os.path.dirname(source))
        for parent, dirnames, filenames in os.walk(source):
            if '__pycache__' in parent:
                continue
            for filename in filenames:
                if filename.endswith('.pyc'):
                    continue
                pathfile = os.path.join(parent, filename)
                arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
                zf.write(pathfile, arcname)
        zf.close()

    def load_project(self, project):
        pass

    def load_spider(self, project, spider):
        pass


class _Zip(_Manager):
    def __init__(self, parent_path, logger=None):
        super(_Zip, self).__init__('zips', parent_path, logger)

    def projects(self, cls=False):
        projects = []
        for _, _, files in os.walk(self.full_path):
            for file in files:
                if file.endswith('.zip'):
                    project_name = file.split('.')[0]
                    module = zipimport.zipimporter(os.path.join(self.full_path, file))
                    module = module.load_module(project_name)
                    _project = {'package': project_name, 'name': module.__name__, 'author': module.__author__,
                                'create_date': module.__date__, 'description': module.__description__,
                                'version': module.__version__, 'spiders': self.spiders(project_name, cls),
                                'doc': module.__doc__, 'from': 'zip', 'path': os.path.join(self.full_path, file)}
                    projects.append(_project)
        return projects

    def spiders(self, project, cls=False):
        _spiders = []
        project_path = os.path.join(self.full_path, '%s.zip' % project)
        module = zipimport.zipimporter(project_path)
        module = module.load_module('%s/spiders' % project)
        for class_name, class_type in inspect.getmembers(module, inspect.isclass):
            spider_class = getattr(module, class_name)
            if spider_class.name and issubclass(spider_class, BaseSpider):
                info = {'name': spider_class.name, 'doc': spider_class.__doc__, 'project_path': project_path}
                if cls:
                    info['cls'] = spider_class
                _spiders.append(info)
        return _spiders

    def unzip(self, project):
        zf = os.path.join(self.full_path, '%s.zip' % project)
        if not os.path.exists(zf):
            raise FileNotFoundError("zip文件不存在")
        zf = zipfile.ZipFile(zf, 'r')
        for file in zf.namelist():
            zf.extract(file, os.path.join(self.full_path, '..', 'sources', project))
        zf.close()

    def load_project(self, project):
        pass

    def load_spider(self, project, spider):
        pass


class SpiderManager(object):
    _source_module = _Source
    _zip_module = _Zip

    def __init__(self, loop=None, spider_path='spiders', home_path=None):
        self.loop = loop or asyncio.get_event_loop()
        self.logger = None
        self._spider_path = spider_path
        self.tasks = []
        self.home_path = home_path or os.path.abspath('.')
        self.spider_path = os.path.join(self.home_path, self._spider_path)
        if not os.path.exists(self.spider_path):
            os.makedirs(self.spider_path, exist_ok=True)
        self.setup_logger()
        self.source_control = self._source_module(self.spider_path, self.logger)
        self.zip_control = self._zip_module(self.spider_path, self.logger)
        self._sync()

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

    def projects(self, cls=False):
        _projects = self.zip_control.projects(cls=cls)

        def _filter(p):
            for _project in _projects:
                if _project.get('name') == p.get('name'):
                    return False
            return True

        _projects += filter(_filter, self.source_control.projects(cls=cls))
        return _projects

    def spiders(self, project, cls=False):
        return self.zip_control.spiders(project, cls=cls) or self.source_control.spiders(project, cls=cls)

    def load_spider(self, project, spider):  # spider name
        spiders = self.spiders(project, True)
        for _spider in spiders:
            if _spider['name'] == spider:
                return _spider
        return None

    def setup_spider(self, project, spider):
        """
        setup a spider
        :param spider: name
        :return:
        """
        spider_info = self.load_spider(project, spider)
        spider_cls = spider_info.get('cls')
        spider_path = spider_info.get('project_path')
        print(spider_info)
        return spider_cls.setup_from_path(spider_path)

    def zip(self, project):
        self.source_control.zip(project)

    def unzip(self, project):
        self.zip_control.unzip(project)

    def get_project(self, project):
        pass

    def _sync(self):
        """同步source 到 zip"""
        _projects = self.zip_control.projects()

        def _filter(p):
            for _project in _projects:
                if _project.get('name') == p.get('name'):
                    return False
            return True

        for source in filter(_filter, self.source_control.projects()):
            self.source_control.zip(source.get('package'))
