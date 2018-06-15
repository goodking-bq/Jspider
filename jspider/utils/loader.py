# coding:utf-8
from __future__ import absolute_import, unicode_literals
import os, importlib

__author__ = "golden"
__date__ = '2018/5/28'


def load_class(name):
    paths = name.split('.')
    modes, class_name = paths[:-1], paths[-1]
    module = importlib.import_module('.'.join(modes))
    return getattr(module, class_name)


def lazy_load_module(path):
    if os.path.isdir(path):
        path = os.path.join(path, '__init__.py')
    package_name = os.path.basename(path)
    spec = importlib.util.spec_from_file_location(package_name, path)
    module = spec.loader.load_module()
    return module


def lazy_load_class(name, package_path=None):
    """
    :param name: pipeline.ConsolePipeLine
    :param package_path:
    :return:
    """
    try:
        module = load_class(name)
        return module
    except Exception as e:
        if package_path:
            names = name.split('.')
            full_path = os.path.join(package_path, *names[:1]) + '.py'
            package = lazy_loader(full_path)
            return getattr(package, names[-1])
        raise
