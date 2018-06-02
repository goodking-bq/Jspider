# coding:utf-8
from __future__ import absolute_import, unicode_literals

__author__ = "golden"
__date__ = '2018/5/29'
import asyncio


async def loop1():
    while True:
        print('loop1')
        await asyncio.sleep(1)


async def loop2():
    while True:
        print('loop2')
        await asyncio.sleep(1)


loop = asyncio.get_event_loop()
asyncio.ensure_future(loop1())
asyncio.ensure_future(loop2())
loop.run_forever()
