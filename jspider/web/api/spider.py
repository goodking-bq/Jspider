# coding:utf-8
from __future__ import absolute_import, unicode_literals
from sanic.views import HTTPMethodView
from sanic.response import json

__author__ = "golden"
__date__ = '2018/6/25'


class ProjectsApi(HTTPMethodView):
    async def get(self, req):
        app = req.app
        res = app.manager.projects()
        return json(res)


class ProjectApi(HTTPMethodView):
    async def get(self, req):
        app = req.app
        file = req.args.get('file')
        if file:
            pass
        else:
            return json('')


class SpidersApi(HTTPMethodView):
    async def get(self, req, project):
        app = req.app
        return json(app.manager.spiders(project))


class SpiderApi(HTTPMethodView):
    async def get(self, req, project, spider):
        action=req.args.get('action')
        spider = req.manager.setup_spider(project, spider)
        await spider.start_requests()  # push url to request queue

    async def put(self, req, project, spider):
        "run a spider"
        pass
