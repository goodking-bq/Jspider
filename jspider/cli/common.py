# coding:utf-8
from __future__ import absolute_import, unicode_literals
import click, asyncio
from jspider.manager import Manager

__author__ = "golden"
__date__ = '2018/6/11'


class Public(object):
    def __init__(self):
        self.loop = None
        self.manager = None
        self.debug = False
        self.asyncio = asyncio


def spider_path_option(f):
    def callback(ctx, param, spider_path):
        pub = ctx.ensure_object(Public)
        pub.manager = Manager(pub.loop, spider_path=spider_path)
        return spider_path

    return click.option('--spider-path', type=click.Path(exists=True, dir_okay=True), default='./spiders',
                        help='spider path',
                        expose_value=False,
                        callback=callback)(f)


def loop_option(f):
    def callback(ctx, param, value):
        pub = ctx.ensure_object(Public)
        if value:
            import uvloop
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        loop = asyncio.get_event_loop()
        pub.loop = loop
        return value

    return click.option('-u', '--uvloop', is_flag=True,
                        help='loop type',
                        expose_value=False, is_eager=True,
                        callback=callback)(f)


def debug_option(f):
    def callback(ctx, param, value):
        print('debug', value)
        pub = ctx.ensure_object(Public)
        pub.debug = value
        pub.loop.set_debug(value)
        return value

    return click.option('-d', '--debug', is_flag=True,
                        help='open debug',
                        expose_value=False,
                        callback=callback)(f)


def common_options(f):
    f = debug_option(f)
    f = loop_option(f)
    f = spider_path_option(f)
    return f


common_pass = click.make_pass_decorator(Public, ensure=True)
