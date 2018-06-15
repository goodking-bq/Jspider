# coding:utf-8
from __future__ import absolute_import, unicode_literals
from jspider.spider import Spider

__author__ = "golden"
__date__ = '2018/6/4'


class QbSpider(Spider):
    """糗百"""
    name = "qb"
    start_urls = ['https://www.qiushibaike.com/']

    async def parse(self, response):
        items = await response.css('.content')
        for item in items:
            msg = item.find('span').text_content().strip()
            await self.item_queue.push({"text": msg})
        next_page = await response.css('.next')
        url = next_page.parent().attr('href')
        if '下一页' in next_page('span').text():
            url = response.url_join(url)
            await self.make_request(url)


class Tspider(object):
    name = "tspider"
