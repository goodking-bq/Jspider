# coding:utf-8

__author__ = "golden"
__date__ = '2018/6/29'

PID_FILE = "jspider.pid"
LOG_PATH = "log"
SPIDER_PATH = 'spiders'
WEB_DOMAIN = '193.168.4.101'
WEB_SERVER = {
    'host': '0.0.0.0',
    'port': 8081,
    'debug': True,
    'ssl': None,
    'sock': None,
    'protocol': None,
    'backlog': 100,
    'stop_event': None,
    'access_log': True
}
WEB_CONFIG = {  # key must upper
    "KEEP_ALIVE": True,
    "AUTH_LOGIN_ENDPOINT": "login"
}
NODE = {
    'name': ''
}
