# coding:utf-8
from __future__ import absolute_import, unicode_literals
import click
from jspider.cli.common import common_options, common_pass
from jspider.cli.spider import list_obj
from jspider.manager import Multiprocessing

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
def web_server(pub, host, port):
    """run http server"""
    pub.manager.add_web(host, port, pub.debug)
    pub.manager.run_forever()


@cli.command()
@click.argument('name')
@click.option('-f', '--run-forever', is_flag=True, help="run forever")
@click.option('-D', '--daemon', is_flag=True, help="run background")
@common_options
@common_pass
def run(pub, name, run_forever, daemon):
    """run spider"""
    spider = pub.manager.setup_spider(name, run_forever=run_forever)
    if spider:
        spider.run()
    else:
        print("spider {name} not exist".format(name=name))


@cli.command()
def init():
    """init current dir as jspider"""
    pass


@cli.command()
@click.option('-w', '--web', is_flag=True, help="run web")
@click.option('-s', '--spider', help="run web", multiple=True)
@click.option('-a', '--all', is_flag=True, help="run all")
@click.option('-p', '--project', help="run project", multiple=True)
@click.option('--smart', is_flag=True, help='run spider when need')
@click.option('-c', '--config-file', type=click.Path(exists=True, dir_okay=True), default='config.py')
@common_options
@common_pass
def start(pub, **kwargs):
    """run something background"""
    click.echo(kwargs)
    manager = Multiprocessing(config=kwargs.get('config_file'))
    if kwargs.get('all'):
        manager.add_web()
        qb = pub.manager.setup_spider('qb')
        manager.add_sub(qb.run, qb.name)
    if kwargs.get('web'):  # web subprocess
        manager.add_web()
    if kwargs.get('spider'):
        pass
    manager.start()


@cli.command()
@click.option('-c', '--config-file', type=click.Path(exists=True, dir_okay=True), default='config.py')
def stop(**kwargs):
    """stop"""
    manager = Multiprocessing(config=kwargs.get('config_file'))
    manager.stop()


cli.add_command(list_obj)
