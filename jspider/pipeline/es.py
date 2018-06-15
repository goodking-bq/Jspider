# coding:utf-8
from __future__ import absolute_import, unicode_literals
from jspider.pipeline.base import BasePipeLine
from elasticsearch import Elasticsearch

__author__ = "golden"
__date__ = '2018/6/13'


class EsPipeLine(BasePipeLine):
    """
    pipe to es
    need package elasticsearch
    """

    @classmethod
    def from_spider(cls, spider):
        es_hosts = spider.config.get('ES_HOSTS')
        es_index = spider.config.get('ES_CONFIG')
        es_options = spider.config.get('ES_OPTIONS')
        pipe = super(EsPipeLine, cls).from_spider(spider)
        pipe.es = Elasticsearch(es_hosts, **es_options)
        pipe.index = es_index
        return pipe

    async def process_item(self, item):
        self.es.index(index=self.index, body=item)
