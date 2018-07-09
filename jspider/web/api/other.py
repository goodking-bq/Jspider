# coding:utf-8
from __future__ import absolute_import, unicode_literals
from sanic.views import HTTPMethodView
from sanic.response import json

__author__ = "golden"
__date__ = '2018/7/9'


class MenusApi(HTTPMethodView):
    @classmethod
    async def get(cls, req):
        return json([
            {'header': 'Apps'},
            {
                'title': '首页',
                'group': 'apps',
                'icon': 'dashboard',
                'name': 'Dashboard',
            },
            {
                'title': '项目',
                'group': 'apps',
                'icon': 'folder',
                'name': 'Project',
            },
        ])
