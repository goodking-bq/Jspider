# coding:utf-8
from __future__ import absolute_import, unicode_literals
import click
from jspider.manager import Manager
import asyncio
from collections import namedtuple

__author__ = "golden"
__date__ = '2018/6/9'


@click.group()
@click.option('--spider-path', default='./spiders', help='spider path')
@click.pass_context
def cli(ctx, spider_path):
    obj = namedtuple('obj', ['loop', 'manager', 'asyncio'])
    loop = asyncio.get_event_loop()
    manager = Manager(loop, spider_path=spider_path)
    ctx.obj = obj(loop=loop, manager=manager, asyncio=asyncio)


@cli.command()
@click.option('-H', '--host', default='127.0.0.1', help="bind address")
@click.option('-P', '--port', default=5000, help="bind port")
@click.option('-d', '--debug', is_flag=True, help="bind port")
@click.pass_obj
def web(obj, host, port, debug):
    """run http server"""
    obj.manager.add_web(host, port, debug)
    obj.manager.run()

 
