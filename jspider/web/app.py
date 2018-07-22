# coding:utf-8
from __future__ import absolute_import, unicode_literals
from sanic import Sanic
from sanic.response import html, json
import os
from .api import bp
from sanic_cors import CORS
from sanic_auth import Auth, User

__author__ = "golden"
__date__ = '2018/6/1'


def app_creator(config: dict, manager=None):
    app = Sanic(__name__)
    app.manager = manager
    app.config.update(config)
    app.static('/static', '/root/golden/jspider/jspider/web/dist')
    app.blueprint(bp)
    app.node_state = {}
    cors = CORS(app, supports_credentials=True)
    auth = Auth(app)
    auth.login_endpoint='login'
    @app.listener('before_server_start')
    async def setup_db(app, loop):
        app.spider_state = app.manager.projects()

    @app.middleware('request')
    async def add_session_to_request(request):
        request['session'] = {}

    # app.config.from_pyfile()
    @app.route("/")
    async def index(request):
        htm = os.path.join(app.config['HOME_PATH'], 'jspider', 'web', 'dist', 'index.html')
        with open(htm, 'r+') as f:
            return html(f.read())

    @app.route('/heart_beat/', methods=['GET'])
    async def heart_beat(req):
        name = req.args.get('name')
        sys_type = req.args.get('sys_type')
        sys_version = req.args.get('sys_version')
        if name not in app.node_state:
            app.node_state[name] = {"sys_type": sys_type, 'sys_version': sys_version,
                                    'spider_state': app.manager.projects()}
            app.node_state[name].update(status=1)
        return json({'name': name, 'spider_state': app.node_state[name]['spider_state']})  # 1需要更新

    @app.route('/login', methods=['POST'])
    async def login(request):
        message = ''
        username = request.form.get('username')
        password = request.form.get('password')
        # fetch user from database
        user = User(id=1, name=username)
        if user:
            auth.login_user(request, user)
            return json({"status": 0, "msg": "%s login success" % username})

    @app.route('/menus/', methods=['GET'])
    @auth.login_required
    async def menus(req):
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
            {
                'title': '日志',
                'group': 'apps',
                'icon': 'folder',
                'name': 'log',
            },
        ])

    @app.route('/logout/', methods=['GET'])
    @auth.login_required
    async def logout(req):
        auth.logout_user(req)
        return json(json({"status": 0, "msg": "logout success"}))

    return app
