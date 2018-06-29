# coding:utf-8
from __future__ import absolute_import, unicode_literals
from jspider.manager.deamon import Daemon
import multiprocessing

__author__ = "golden"
__date__ = '2018/6/26'
import time
import asyncio


async def task_async():
    while True:
        print('task async running')
        await asyncio.sleep(1)


class Main(Daemon):
    def __init__(self):
        super(Main, self).__init__(pid_file='/tmp/aa.pid', stdout='/tmp/aa.log')

    def run(self):
        def task():
            while True:
                print('task running at %s' % time.time())
                time.sleep(2)

        def task2():
            loop = asyncio.new_event_loop()
            asyncio.run_coroutine_threadsafe(task_async(), loop)
            asyncio.set_event_loop(loop)
            loop.run_forever()

        p1 = multiprocessing.Process(target=task)
        p2 = multiprocessing.Process(target=task2)
        p1.start()
        p2.start()
        p1.join()
        p2.join()


if __name__ == '__main__':
    m = Main()
    m.start()
