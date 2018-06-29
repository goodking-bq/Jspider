# coding:utf-8
from __future__ import absolute_import, unicode_literals
from sanic_restful import Resource

__author__ = "golden"
__date__ = '2018/6/25'


class ProjectsApi(Resource):
    async def get(self, req):
        app = req.app
        return app.manager.list_projects()


class SpidersApi(Resource):
    async def get(self, req):
        app = req.app
        return app.manager.list_spiders()
