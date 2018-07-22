# coding:utf-8
from __future__ import absolute_import, unicode_literals

__author__ = "golden"
__date__ = '2018/7/20'
from jspider.web.app import app_creator
from jspider.utils.config import Config
from jspider.manager.spider import SpiderManager
if __name__ == '__main__':
    config = Config()
    config.from_pyfile('config.py')
    app = app_creator(config)
    app.manager = SpiderManager()
    app.run(debug=True, host='0.0.0.0', port=8081)
