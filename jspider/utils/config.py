# coding:utf-8
from __future__ import absolute_import, unicode_literals
import os, types

__author__ = "golden"
__date__ = '2018/6/13'


class Config(dict):
    def __init__(self, defaults=None):
        super().__init__(defaults or {})

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError as ke:
            raise AttributeError("Config has no '{}'".format(ke.args[0]))

    def __setattr__(self, attr, value):
        self[attr] = value

    def from_pyfile(self, filename):
        module = types.ModuleType('config')
        module.__file__ = filename
        try:
            with open(filename) as config_file:
                exec(compile(config_file.read(), filename, 'exec'),
                     module.__dict__)
        except IOError as e:
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        self.from_object(module)
        return True

    def from_object(self, obj):
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)
