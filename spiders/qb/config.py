# coding:utf-8
from __future__ import absolute_import, unicode_literals

__author__ = "golden"
__date__ = '2018/6/4'

DOWNLOADER_CLS = 'jspider.downloader.AioHttpDownloader'
QUEUE_CLS = 'jspider.queue.DefaultQueue'
PIPE_LINE_CLS = 'jspider.pipeline.ConsolePipeLine'
REQUEST_QUEUE_CLS = 'jspider.queue.redis.RedisQueue'
ES_HOSTS = ['localhost']
ES_INDEX = 'jspider'
ES_OPTIONS = {}
REDIS = {
    "host": "193.168.4.101",
    "port": 6379,
    "db": 3
}
