# coding:utf-8
from __future__ import absolute_import, unicode_literals
from sanic.blueprints import Blueprint
from sanic_restful import Api
from . import spider

__author__ = "golden"
__date__ = '2018/6/25'

bp = Blueprint(__name__, '/api/')
api = Api(bp)

api.add_resource(spider.ProjectsApi, 'projects/')
api.add_resource(spider.SpidersApi, 'spiders/')
