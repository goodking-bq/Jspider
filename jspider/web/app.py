# coding:utf-8
from __future__ import absolute_import, unicode_literals
from sanic import Sanic
from sanic.response import json

__author__ = "golden"
__date__ = '2018/6/1'
app = Sanic()


@app.route("/")
async def test(request):
    return json({"hello": "world"})
