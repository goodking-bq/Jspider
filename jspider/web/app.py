# coding:utf-8
from __future__ import absolute_import, unicode_literals
from sanic import Sanic
from sanic.response import html, json
import os
from .api import bp

__author__ = "golden"
__date__ = '2018/6/1'


def app_creator(config):
    app = Sanic(__name__)
    app.manager = None
    app.config.update(config)
    app.static('/static', '/root/golden/jspider/jspider/web/dist')
    app.blueprint(bp)

    # app.config.from_pyfile()
    @app.route("/")
    async def index(request):
        htm = os.path.join(app.config['HOME_PATH'], 'jspider', 'web', 'dist', 'index.html')
        with open(htm, 'r+') as f:
            return html(f.read())

    @app.route('/login', methods=['POST'])
    async def login(request):
        return json(dict(token="asdfasdfasdf"))

    return app
