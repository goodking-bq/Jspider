# coding:utf-8
import asyncio
from jspider.spider.spider import Spider
from jspider.downloader.aiohttp_downloader import AioHttpDownloader
from jspider.logger import setup_logger
from jspider.utils.loader import load_class
import os

__author__ = "golden"
__date__ = '2018/5/26'


def main():
    spider = Spider(downloader_cls='jspider.downloader.RequestsDownloader', queue_cls='jspider.queue.DefaultQueue')
    spider.run()


if __name__ == '__main__':
    main()
