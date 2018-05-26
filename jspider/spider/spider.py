# coding:utf-8
from __future__ import absolute_import, unicode_literals
from jspider.spider.base import BaseSpider

__author__ = "golden"
__date__ = '2018/5/26'


class Spider(BaseSpider):
    start_urls = ['http://www.baidu.com']
    name = 'spider'

    async def run(self):
        for url in self.start_urls:
            html = await self.downloader.download(self, url)
            self.logger.debug(html)
