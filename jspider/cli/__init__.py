# coding:utf-8
from __future__ import absolute_import, unicode_literals
import click
from jspider.manager import Manager
import asyncio
from collections import namedtuple

__author__ = "golden"
__date__ = '2018/6/9'


class Public(object):
    def __init__(self):
        self.loop = None
        self.manager = None
        self.asyncio = asyncio


def spider_path_option(f):
    def callback(ctx, param, spider_path):
        pub = ctx.ensure_object(Public)
        loop = pub.loop or asyncio.get_event_loop()
        pub.loop = loop
        pub.manager = Manager(loop, spider_path=spider_path)
        return spider_path

    return click.option('--spider-path', type=click.Path(exists=True, dir_okay=True), default='./spiders',
                        help='spider path',
                        expose_value=False,
                        callback=callback)(f)


def common_options(f):
    f = spider_path_option(f)
    return f


public = click.make_pass_decorator(Public, ensure=True)


@click.group()
def cli():
    pass


@cli.command()
@click.option('-H', '--host', default='127.0.0.1', help="bind address")
@click.option('-P', '--port', default=5000, help="bind port")
@click.option('-d', '--debug', is_flag=True, help="bind port")
@common_options
@public
def web(pub, host, port, debug):
    """run http server"""
    pub.manager.add_web(host, port, debug)
    pub.manager.run()
