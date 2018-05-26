# coding:utf-8
from __future__ import absolute_import, unicode_literals
from jspider.downloader.base import BaseDownloader
from jspider.http.response import Response
import aiohttp

__author__ = "golden"
__date__ = '2018/5/26'


class AioHttpDownloader(BaseDownloader):
    def __init__(self):
        super(AioHttpDownloader, self).__init__()

    async def download(self, spider, request, proxy=None, user_agent=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(request.url) as response:
                status, body = response.status, await response.text()
                return Response(response.url, body, status, request)
