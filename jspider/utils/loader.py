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
