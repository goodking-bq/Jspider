# coding:utf-8
from __future__ import absolute_import, unicode_literals
import click
from jspider.cli.common import common_options, common_pass
from jspider.cli.spider import list_obj

__author__ = "golden"
__date__ = '2018/6/11'

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command()
@click.option('-H', '--host', default='127.0.0.1', help="bind address")
@click.option('-P', '--port', default=5000, help="bind port")
@common_options
@common_pass
def web(pub, host, port):
    """run http server"""
    pub.manager.add_web(host, port, pub.debug)
    pub.manager.run_forever()


@cli.command()
@click.argument('name')
@common_options
@common_pass
def run(pub, name):
    """run spider"""
    spider = pub.manager.setup_spider(name)
    if spider:
        spider.run()
    else:
        print("spider {name} not exist".format(name=name))


cli.add_command(list_obj)
