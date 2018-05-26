# coding:utf-8
from __future__ import absolute_import, unicode_literals
from jspider.downloader.base import BaseDownloader
import aiohttp

__author__ = "golden"
__date__ = '2018/5/26'


class AioHttpDownloader(BaseDownloader):
    def __init__(self):
        super(AioHttpDownloader, self).__init__()

    async def download(self, spider, url, proxy=None, user_agent=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
                return text
