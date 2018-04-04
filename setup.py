#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '启动服务'
__author__ = 'JN Zhang'
__mtime__ = '2017/12/21'
"""
import multiprocessing
import threading
import datetime
from time import sleep

from api_tkdata import start_api_tkdata
from core.data_crawl import ENDataCrawl
from t_redis.redis_manager import RedisManager

time_interval = 60


def start_service():
    pool = multiprocessing.Pool(processes=2)
    # 启动数据接口
    pool.apply_async(start_api_tkdata)
    # 启动定时器
    pool.apply_async(fun_timer)
    pool.close()
    pool.join()


# 定时器(启动服务时调用)
def fun_timer():
    # 每分钟与系统进行对时(数据更新时间为16:00 & 24:00)
    cur_time = datetime.datetime.now().time()
    print(cur_time)
    hour = str(cur_time).split(":")[0]
    minute = str(cur_time).split(":")[1]
    if (hour == "16" or hour == "00") and minute == "00":
        dc = ENDataCrawl()
        dc.start_crawl()
        # 爬虫业务完成后同步数据到redis
        sleep(time_interval)
        rm = RedisManager()
        rm.update_data()
        # 计算w_macd并同步到redis
    global timer
    timer = threading.Timer(time_interval, fun_timer)
    timer.start()


if __name__ == '__main__':
    start_service()
