# coding:utf-8
from __future__ import absolute_import, unicode_literals
from sanic.blueprints import Blueprint
from . import spider, other

__author__ = "golden"
__date__ = '2018/6/25'

bp = Blueprint(__name__, '/api/')
bp.add_route(spider.SpidersApi.as_view(), '<project:[A-z]+>/spiders/')
bp.add_route(spider.ProjectsApi.as_view(), 'projects/')
bp.add_route(other.MenusApi.as_view(), 'menus/')
