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

from api_tkdata import start_api_tkdata
from core.c_strategy.strategy_3 import TsStrategy3
from core.data_crawl import ENDataCrawl
from core.wmacd_utils import WmacdUtils
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
    # 每分钟与系统进行对时(数据更新时间为16:00 & 22:00)
    cur_time = datetime.datetime.now().time()
    print(cur_time)
    hour = str(cur_time).split(":")[0]
    minute = str(cur_time).split(":")[1]
    if (hour == "16" or hour == "22") and minute == "00":
        if datetime.datetime.strptime(str(datetime.datetime.now().date()), "%Y-%m-%d").weekday() in [5, 6]:
            # 开始指标数据计算业务
            wu = WmacdUtils()
            wu.update_w_macd()
            # 同步指标数据到redis
            st3 = TsStrategy3()
            st3.update_redis(datetime.datetime.now().date())
        else:
            # 开始基础数据爬虫业务
            dc = ENDataCrawl()
            dc.start_crawl()
            # 同步基础数据到redis
            rm = RedisManager()
            rm.update_data()
    global timer
    timer = threading.Timer(time_interval, fun_timer)
    timer.start()


if __name__ == '__main__':
    start_service()
