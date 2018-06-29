# coding:utf-8
from __future__ import absolute_import, unicode_literals
import time
from jspider.manager import Multiprocessing
import multiprocessing
import asyncio
import aredis

__author__ = "golden"
__date__ = '2018/6/25'


def main_test():
    while True:
        print('main run ing')
        time.sleep(3)


def test():
    def test1(i):
        while True:
            print('sub run ing %s' % i)
            time.sleep(3)

    i = 0
    while True:
        print('run ing %s' % i)
        time.sleep(3)
        p = multiprocessing.Process(target=test1, args=[i])
        p.daemon = True
        p.start()
        i += 1


async def test1():
    redis = aredis.StrictRedis('193.168.4.101', db=4)
    print('test1 running')
    while True:
        print('test1 running')
        await redis.incr('aa')
        await asyncio.sleep(1)


asyncio.isfuture(test1)
asyncio.iscoroutinefunction(test1)
if __name__ == '__main__':
    p = Multiprocessing(pid_file='/tmp/jspider.pid')
    p.add_sub(test1, 'test1')
    p.start()
