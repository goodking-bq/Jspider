# coding:utf-8
from __future__ import absolute_import, unicode_literals
import hashlib
import random

__author__ = "golden"
__date__ = '2018/6/12'

# Python 3 program to build Bloom Filter
# Install mmh3 and bitarray 3rd party module first
# pip install mmh3
# pip install bitarray
import math
import hashlib


class BloomFilter(object):
    """
    """

    def __init__(self, max_elements, error_rate, array_cls=None):
        """
        :param max_elements: 预计多少个数据
        :param error_rate: 错误率
        """
        self.error_rate = error_rate
        self.max_elements = max_elements

        # Size of bit array to use
        self.size = self.get_size()

        # number of hash functions to use
        self.hash_count = self.get_hash_count()
        self._size = 0
        if array_cls is not False:
            if array_cls:
                self.array = array_cls(self.size)
            else:
                from bitarray import bitarray
                self.array = bitarray(self.size)
            self.array.setall(0)

    def set_array(self, array):
        self.array = array

    def add(self, item):
        """
        添加一个元素
        :param item: 元素
        :return: if array change return TRUE
        """
        result = False
        for func in self.hash_funcs(self.hash_count):
            digest = func(item) % self.size
            if self.array[digest] == 1:
                pass
            else:
                self.array[digest] = 1
                result = True
        if result:
            self._size += 1
        return result

    async def async_add(self, item):
        """
        添加一个元素
        :param item: 元素
        :return:
        """
        result = False
        for func in self.hash_funcs(self.hash_count):
            digest = func(item) % self.size
            if await self.array.get(digest) == 1:
                pass
            else:
                await self.array.set(digest, 1)
                result = True
        if result:
            self._size += 1
        return result

    def __contains__(self, item):
        for func in self.hash_funcs(self.hash_count):
            digest = func(item) % self.size
            if self.array[digest] == 0:
                return False
        return True

    def get_size(self):
        """
         最佳的bit长度计算公式:  m = -(max_elements * lg(error_rate)) / (lg(2)^2)
        """

        m = -(self.max_elements * math.log(self.error_rate)) / (math.log(2) ** 2)
        return int(m)

    def get_hash_count(self):
        """
            最佳的hash方法的个数 计算公式：k = (size/error_rate) * lg(2)
        """
        k = (self.size / self.max_elements) * math.log(2)
        return int(k)

    def hash_funcs(self, number):
        def _hash_func(i):
            def __hash_func(item):
                _num = i % 20 + 16
                a = int(hashlib.sha1(item.encode('utf-8')).hexdigest(), _num) % self.size
                b = int(hashlib.sha1(item.encode('utf-8')).hexdigest(), _num) % self.size
                return a + b * _num

            return __hash_func

        for n in range(number):
            yield _hash_func(n)

    def __len__(self):
        return self._size

    async def async_clean(self):
        await self.array.delete()

    def clean(self):
        pass


if __name__ == '__main__':
    b = BloomFilter(20000, 0.1)
    print(b.add('a'))
    print(b.add('b'))
    print(len(b))
