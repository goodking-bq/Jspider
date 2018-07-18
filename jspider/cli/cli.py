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
@click.option('-c', '--config-file', type=click.Path(exists=True, dir_okay=True), default='config.py')
@common_options
@common_pass
def web_server(pub, host, port, config_file):
    """run http server"""
    manager = Multiprocessing(config=config_file)
    manager.config['WEB_SERVER']['host'] = host
    manager.config['WEB_SERVER']['port'] = port
    manager.add_web()
    manager.start()


@cli.command()
@click.argument('project')
@click.argument('spider')
@click.option('-f', '--run-forever', is_flag=True, help="run forever")
@click.option('-D', '--daemon', is_flag=True, help="run background")
@common_options
@common_pass
def run(pub, project, spider, run_forever, daemon):
    """run spider"""
    spider = pub.manager.setup_spider(project, spider)
    if spider:
        spider.run()
    else:
        print("spider {project}.{name} not exist".format(project, spider))


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


@cli.command()
@click.option('-c', '--config-file', type=click.Path(exists=True, dir_okay=True), default='config.py')
def restart(**kwargs):
    """restart """
    manager = Multiprocessing(config=kwargs.get('config_file'))
    manager.stop()
    manager.add_web()
    manager.start()


cli.add_command(list_obj)
