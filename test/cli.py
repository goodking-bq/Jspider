# coding:utf-8
from __future__ import absolute_import, unicode_literals
import click

__author__ = "golden"
__date__ = '2018/6/9'
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('--port', default=8000)
def runserver(port):
    click.echo('Serving on http://127.0.0.1:%d/' % port)


if __name__ == '__main__':
    cli(default_map={
        'runserver': {
            'port': 5000
        }
    })
