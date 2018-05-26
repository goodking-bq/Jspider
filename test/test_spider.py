# coding:utf-8
import asyncio
from jspider.spider.spider import Spider
from jspider.downloader.aiohttp_downloader import AioHttpDownloader
from jspider.logger import setup_logger
import os

__author__ = "golden"
__date__ = '2018/5/26'


def main():
    setup_logger(os.path.dirname(os.path.abspath(__file__)), 'main')
    asyncio.ensure_future(Spider(downloader=AioHttpDownloader).run())
    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except KeyboardInterrupt as e:
        print(asyncio.gather(*asyncio.Task.all_tasks()).cancel())
        loop.stop()
        loop.run_forever()
    finally:
        loop.close()


if __name__ == '__main__':
    main()
