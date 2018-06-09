# coding:utf-8
from __future__ import absolute_import, unicode_literals
from jspider.spider import Spider
import asyncio
from jspider.manager import Manager

__author__ = "golden"
__date__ = '2018/6/2'


class QbSpider(Spider):
    name = 'qb'
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


if __name__ == '__main__':
    manager = Manager()
    sp = QbSpider()
    manager.add_spider(sp)
    manager.run()
