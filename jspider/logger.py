# coding:utf-8
from __future__ import absolute_import, unicode_literals
import logging
import logging.config
import os

__author__ = "golden"
__date__ = '2018/5/26'


def setup_logger(path_dir, name):
    standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                      '[%(levelname)s][%(message)s]'  # 其中name为getlogger指定的名字

    simple_format = '%(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)d: %(message)s'

    id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'
    logfile_dir = path_dir or os.path.dirname(os.path.abspath(__file__))  # log文件的目录
    if not os.path.isdir(logfile_dir):
        os.mkdir(logfile_dir)
    # log文件的全路径
    logfile_path = os.path.join(logfile_dir, name + '.log')
    LOGGING_DIC = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': standard_format
            },
            'simple': {
                'format': simple_format
            },
        },
        'filters': {},
        'handlers': {
            # 打印到终端的日志
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',  # 打印到屏幕
                'formatter': 'simple'
            },
            # 打印到文件的日志,收集info及以上的日志
            'default': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
                'formatter': 'standard',
                'filename': logfile_path,  # 日志文件
                'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
                'backupCount': 5,
                'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
            },
        },
        'loggers': {
            # logging.getLogger(__name__)拿到的logger配置
            '': {
                'handlers': ['default', 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
                'level': 'DEBUG',
                'propagate': True,  # 向上（更高level的logger）传递
            },
        },
    }
    logging.config.dictConfig(LOGGING_DIC)  # 导入上面定义的logging配置
    logger = logging.getLogger(name)  # 生成一个log实例
