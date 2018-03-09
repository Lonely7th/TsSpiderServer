#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '缓存管理类'
__author__ = 'JN Zhang'
__mtime__ = '2018/2/28'
"""
import datetime

import operator

import redis

from config import mod_config

from logs.logs_manager import add_error_logs, add_info_logs
from mongo_db.mongodb_manager import DBManager


def cmp_datetime(a, b):
    a_datetime = datetime.datetime.strptime(a, "%Y-%m-%d")
    b_datetime = datetime.datetime.strptime(b, "%Y-%m-%d")
    if a_datetime > b_datetime:
        return -1
    elif a_datetime < b_datetime:
        return 1
    else:
        return 0


class RedisManager:
    def __init__(self):
        # host是redis主机，需要redis服务端和客户端都启动
        self.pool = redis.ConnectionPool(host=mod_config.get_config("redis", "redis_host"), port=mod_config.get_config("redis", "redis_port"), decode_responses=True)
        self.r = redis.Redis(connection_pool=self.pool)

    def update_data(self):
        # 将mongodb中的数据同步到redis中
        add_info_logs("redis_start", "-开始同步缓存-")
        dm = DBManager("tk_details")
        code_list = dm.find_by_id("")
        for item in code_list:
            try:
                code = item["code"][:6]
                _result = dm.find_by_id(item["code"])
                sorted_result = sorted(_result["price_list"], cmp=cmp_datetime, key=operator.itemgetter("cur_timer"))
                self.r.set(code, sorted_result[:100])
            except Exception:
                add_error_logs("redis_error", "501", item["code"])
                continue
        add_info_logs("redis_close", "-结束同步缓存-")

    def get_data(self, tk_code=""):
        if tk_code:
            _result = self.r.get(tk_code)
            if _result:
                return _result
        return []


if __name__ == "__main__":
    rm = RedisManager()
    rm.update_data()
