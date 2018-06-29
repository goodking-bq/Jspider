# coding:utf-8
from __future__ import absolute_import, unicode_literals
from sanic import Sanic
from sanic.response import html, json
import os
from .api import bp

__author__ = "golden"
__date__ = '2018/6/1'


def app_creator(config):
    app = Sanic()
    app.manager = None
    app.config.from_object(config)
    app.blueprint(bp)

    # app.config.from_pyfile()
    @app.route("/")
    async def index(request):
        base = os.path.basename(__file__)
        htm = open(os.path.basename(__file__))
        return html('')

    # @app.route("/")
    # async def test(request):
    #     spider = app.manager.setup_spider('qb')
    #     if spider:
    #         app.manager.add_spider(spider)
    #     else:
    #         print("spider {name} not exist".format(name='qb'))
    #     return json({"hello": "world"})

    @app.route('/login', methods=['POST'])
    async def login(request):
        return json(dict(token="asdfasdfasdf"))

    return app
