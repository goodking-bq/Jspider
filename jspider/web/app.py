# coding:utf-8
from __future__ import absolute_import, unicode_literals
from sanic import Sanic
from sanic.response import html, json
import os
from .api import bp
from sanic_cors import CORS

__author__ = "golden"
__date__ = '2018/6/1'

node_state = {}


def app_creator(config):
    app = Sanic(__name__)
    app.manager = None
    app.config.update(config)
    app.static('/static', '/root/golden/jspider/jspider/web/dist')
    app.blueprint(bp)
    CORS(app)

    # app.config.from_pyfile()
    @app.route("/")
    async def index(request):
        htm = os.path.join(app.config['HOME_PATH'], 'jspider', 'web', 'dist', 'index.html')
        with open(htm, 'r+') as f:
            return html(f.read())

    @app.route('/login', methods=['POST'])
    async def login(request):
        return json(dict(token="token"))

    @app.route('/heart_beat/', methods=['GET'])
    async def heart_beat(req):
        name = req.args.get('name')
        sys_type = req.args.get('sys_type')
        sys_version = req.args.get('sys_version')
        if name not in node_state:
            node_state[name] = {"sys_type": sys_type, 'sys_version': sys_version}
            node_state[name].update(status=1)
        return json({'name': name, 'status': node_state[name]['status']})  # 1需要更新

    return app
