# coding:utf-8
from __future__ import absolute_import, unicode_literals
from jspider.queue.base import BaseQueue
import aredis
from jspider.utils.bloom_filter import BloomFilter

__author__ = "golden"
__date__ = '2018/6/4'


class RedisBitArray(object):
    def __init__(self, redis=None, key='BIT_ARRAY'):
        self.redis = redis
        self.key = key

    async def get(self, item):
        return await self.redis.getbit(self.key, item)

    async def set(self, key, value):
        await  self.redis.setbit(self.key, key, value)

    async def delete(self):
        await self.redis.delete(self.key)


class RedisQueue(BaseQueue):

    async def push(self, item):
        data = self.dumps(item)
        if hasattr(self, 'bloom_filter'):
            if await self.bloom_filter.async_add(str(item)):
                await self.redis.lpush(self.key, data)
        else:
            await self.redis.lpush(self.key, data)

    async def pop(self):
        data = await self.redis.rpop(self.key)
        if data:
            return self.loads(data)
        return data

    @classmethod
    def from_spider(cls, spider, name, data_format=None, data_filter=None):
        queue = cls(name=name, data_format=data_format, data_filter=data_filter)
        redis_option = spider.config.get('REDIS')
        redis = aredis.StrictRedis(**redis_option)
        queue.redis = redis
        key_name = name
        queue.key = "queue_for_%s_%s" % (spider.name, key_name)
        if data_filter:
            bloom_filter = BloomFilter(20000, 0.1, array_cls=False)
            array = RedisBitArray(redis, "bloom_filter_for_%s_%s" % (spider.name, key_name))
            bloom_filter.set_array(array)
            queue.bloom_filter = bloom_filter
        return queue

    async def is_empty(self):
        res = await self.redis.llen(self.key)
        return res == 0

    async def async_clean(self):
        await  self.bloom_filter.async_clean()
