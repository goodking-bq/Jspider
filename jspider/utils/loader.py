# coding:utf-8
from __future__ import absolute_import, unicode_literals
import os, importlib, zipimport

__author__ = "golden"
__date__ = '2018/5/28'


class Loader(object):
    def __init__(self, from_path: str = None):
        self.from_path = from_path
        print(from_path)
        if os.path.isdir(self.from_path):
            self.path_type = 'dir'
        elif os.path.isfile(self.from_path) and self.from_path.endswith('.zip'):
            self.path_type = 'zip'

    @classmethod
    def __load_class(cls, name: str):
        paths = name.split('.')
        modes, class_name = paths[:-1], paths[-1]
        module = importlib.import_module('.'.join(modes))
        return getattr(module, class_name)

    def lazy_load_module_from_dir(self, name: str = None):
        names = name.split('.')
        if names[-1] == 'py':
            path = os.path.join(self.from_path, *names[:-2], names[-2] + '.py')
        else:
            path = os.path.join(self.from_path, *names[:-1], names[-1] + '.py')
        if not os.path.exists(path):  # 文件不存在
            path = os.path.join(self.from_path, *names, '__init__.py')
        package_name = os.path.basename(path)
        spec = importlib.util.spec_from_file_location(package_name, path)
        module = spec.loader.load_module()
        return module

    def lazy_load_module_from_zip(self, name: str = None):
        package_name = os.path.basename(self.from_path).split('.')[0]
        zf = zipimport.zipimporter(self.from_path)
        names = [package_name] + name.split('.')
        return zf.load_module('/'.join(names))

    def lazy_load_class_from_dir(self, name: str):
        """
        :param name: pipeline.ConsolePipeLine
        :return:
        """
        try:
            module = self.__load_class(name)
            return module
        except ModuleNotFoundError as e:
            names = name.split('.')
            package = self.lazy_load_module_from_dir('.'.join(names[:-1]))
            return getattr(package, names[-1])
        except Exception as e:
            return None

    def lazy_load_class_from_zip(self, name: str):
        try:
            module = self.__load_class(name)
            return module
        except ModuleNotFoundError as e:
            names = name.split('.')
            return getattr(self.lazy_load_module_from_zip('.'.join(names[:-1])), names[-1])
        except Exception as e:
            return None

    def lazy_load_class(self, name):
        if self.path_type == 'dir':
            return self.lazy_load_class_from_dir(name)
        elif self.path_type == 'zip':
            return self.lazy_load_class_from_zip(name)
        return None

    def lazy_load_module(self, name):
        if self.path_type == 'dir':
            return self.lazy_load_module_from_dir(name)
        elif self.path_type == 'zip':
            return self.lazy_load_module_from_zip(name)
        return None


if __name__ == '__main__':
    loader = Loader(r'/root/golden/jspider/spiders/sources')
    print(loader.laze_load_class('qb.__name__'))
