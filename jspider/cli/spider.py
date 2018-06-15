# coding:utf-8
from __future__ import absolute_import, unicode_literals
import click, json
from jspider.cli.common import common_pass, common_options

__author__ = "golden"
__date__ = '2018/6/9'


@click.group(name='list')
def list_obj():
    """show something"""
    pass


@list_obj.command()
@common_options
@common_pass
def projects(pub):
    """show all projects"""
    data = pub.manager.list_projects()
    print(json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False))


@list_obj.command()
@common_options
@common_pass
def spiders(pub):
    """show all spiders"""
    data = pub.manager.list_spiders()
    print(json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False))
