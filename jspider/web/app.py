# coding:utf-8
from __future__ import absolute_import, unicode_literals
from sanic import Sanic
from sanic.response import json

__author__ = "golden"
__date__ = '2018/6/1'
app = Sanic()
app.manager = None


# app.config.from_pyfile()
@app.route("/")
async def test(request):
    spider = app.manager.setup_spider('qb')
    if spider:
        app.manager.add_spider(spider)
    else:
        print("spider {name} not exist".format(name='qb'))
    return json({"hello": "world"})
