# coding:utf-8
from __future__ import absolute_import, unicode_literals
import multiprocessing
import asyncio
from .deamon import Daemon
import os, yaml, sys
import time
import signal
from jspider.web.app import app_creator
from jspider.utils import Config
from jspider.manager.spider import SpiderManager

__author__ = "golden"
__date__ = '2018/6/26'


class AsyncProcess(multiprocessing.Process):
    def __init__(self, target=None, name=None, args=(), kwargs={}):
        super(AsyncProcess, self).__init__(name=name, args=args, kwargs=kwargs)
        signal.signal(signal.SIGINT, self.handle)
        print('process init')
        self.loop = None
        self.daemon = True
        if target:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.add_task(target)

    def run(self):
        if not self.loop:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def stop(self):
        asyncio.run_coroutine_threadsafe(self.loop.stop, self.loop)

    def add_task(self, task):
        asyncio.run_coroutine_threadsafe(task(), self.loop)

    def cancel(self, task):
        asyncio.run_coroutine_threadsafe(task().cancel, self.loop)

    def handle(self, sig, frame):
        print(self.name, sig, frame)


class WebProcess(multiprocessing.Process):
    def __init__(self, server_option, app_option):
        super(WebProcess, self).__init__()
        self.server_option = server_option
        self.app_option = app_option
        self.loop = None
        self.daemon = True
        self.name = 'web-server'

    def run(self):
        app = app_creator(self.app_option)
        app.manager = SpiderManager(spider_path='spiders')
        server = app.create_server(**self.server_option)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        asyncio.run_coroutine_threadsafe(server, self.loop)
        self.loop.run_forever()


class MasterProcess(multiprocessing.Process):
    def __init__(self):
        super(MasterProcess, self).__init__()
        self.name = "manager"

    def run(self):
        def test1(i):
            while True:
                print('sub run ing %s' % i)
                time.sleep(3)

        i = 0
        while True:
            print('run ing %s' % i)
            time.sleep(3)
            # p = multiprocessing.Process(target=test1, args=[i])
            # p.daemon = True
            # p.start()
            # i += 1


class Multiprocessing(Daemon):
    """
    - linux 后台进程
    - 主进程
    - 子进程
    """

    def __init__(self, config, home_path=None):
        self.config = Config()
        if isinstance(config, (bytes, str)):
            self.config.from_pyfile(config)
        else:
            self.config.from_object(config)
        if home_path:
            self.home_path = home_path
        else:
            self.home_path = os.path.abspath('.')
        super(Multiprocessing, self).__init__(pid_file=self.config.get('PID_FILE'))
        self.stdout = os.path.join(self.home_path, self.config.get('LOG_PATH'), 'jspider.log')
        self.pid_file = os.path.join(self.home_path, self.pid_file)
        self.stderr = self.stdout
        self.children = {}
        self.tasks = []
        self._pid = {}

    def run(self):
        task = MasterProcess()
        task.start()
        self.tasks.append(task)
        self.pid = {task.name: task.pid}
        for child in self.children:
            if child == 'web':
                task = WebProcess(server_option=self.config.get('WEB_SERVER'),
                                  app_option=self.config.get('WEB_CONFIG'))
            else:
                if self.children[child]['async']:
                    task = AsyncProcess(target=self.children[child]['target'], name=self.children[child]['name'],
                                        args=self.children[child]['args'], kwargs=self.children[child]['kwargs'])
                else:
                    task = multiprocessing.Process(target=self.children[child]['target'],
                                                   name=self.children[child]['name'],
                                                   args=self.children[child]['args'],
                                                   kwargs=self.children[child]['kwargs'])
            task.start()
            self.tasks.append(task)
            self.pid = {task.name: task.pid}
        self.write_pid_file()
        for task in self.tasks:
            task.join()
        for process in self.tasks:
            process.terminate()
        print('aaa')
        while True:
            for m in self.pid:
                for name in self.pid[m]:
                    os.kill(list(name.values())[0], 2)
            print('signal send')
            time.sleep(2)

    def add_sub(self, target, name, args=(), kwargs={}):
        self.children[name] = {'target': target, 'args': args,
                               'kwargs': kwargs, 'name': name,
                               'async': asyncio.iscoroutinefunction(target)}

    def add_web(self):
        self.children['web'] = True

    @property
    def pid(self):
        return self._pid

    @pid.setter
    def pid(self, value):
        if isinstance(value, dict):
            main_pid = list(self._pid.keys())[0]
            self._pid[main_pid].append(value)
        else:
            self._pid[value] = []

    def write_pid_file(self):
        with open(self.pid_file, 'w+') as f:
            yaml.dump_all([self.pid], f, canonical=False, default_flow_style=False)
