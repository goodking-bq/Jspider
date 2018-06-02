# coding:utf-8
from __future__ import absolute_import, unicode_literals
from jspider.downloader.base import BaseDownloader
from jspider.http.response import Response
import aiohttp
import asyncio

__author__ = "golden"
__date__ = '2018/5/26'


class AioHttpDownloader(BaseDownloader):
    def __init__(self, spider):
        super(AioHttpDownloader, self).__init__(spider)
        self.spider.session = None

    async def download(self, request, proxy=None, user_agent=None):
        # self.set_session()
        async with aiohttp.ClientSession() as session:
            async with session.get(request.url) as response:
                status, body = response.status, await response.text()
                # await  request.callback(Response(response.url, body, status, request))
                print('download ' + request.url)
                return Response(request.url, body, status, request)

    def set_session(self):
        if not self.spider.session:
            session = aiohttp.ClientSession()
            self.spider.session = session
