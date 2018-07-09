# coding:utf-8
from __future__ import absolute_import, unicode_literals
from sanic.views import HTTPMethodView
from sanic.response import json

__author__ = "golden"
__date__ = '2018/6/25'


class ProjectsApi(HTTPMethodView):
    async def get(self, req):
        app = req.app
        res = app.manager.list_projects()
        return json(res)


class SpidersApi(HTTPMethodView):
    async def get(self, req):
        app = req.app
        return json(app.manager.list_spiders())
