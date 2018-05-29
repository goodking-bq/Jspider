# coding:utf-8
from __future__ import absolute_import, unicode_literals
from jspider.downloader.base import BaseDownloader
import requests
from jspider.http.response import Response

__author__ = "golden"
__date__ = '2018/5/29'


class RequestsDownloader(BaseDownloader):
    def __init__(self, spider):
        super(RequestsDownloader, self).__init__(spider)
        self.spider.session = requests.session()

    async def download(self, request, proxy=None, user_agent=None):
        req = requests.get(request.url)
        return Response(req.url, req.content, req.status_code, request)
