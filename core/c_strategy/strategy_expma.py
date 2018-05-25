#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '基于expma的交易策略'
__author__ = 'JN Zhang'
__mtime__ = '2018/5/24'
"""
import datetime
import numpy as np

from bean.tk_wmacd_bean import tkWMacdBean
from mongo_db.mongodb_manager import DBManager
from t_redis.redis_manager import RedisManager


def time_cmp(first_time, second_time):
    return datetime.datetime.strptime(first_time, "%Y-%m-%d") >= datetime.datetime.strptime(second_time, "%Y-%m-%d")


def date_range(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days + 1
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]


class TsStrategyExpma:
    def __init__(self):
        self.db_manager_wm = DBManager("wm_details")

    def get_result(self, ema_12_list, ema_26_list):
        if len(ema_12_list) > 30 and ema_12_list[-1] > ema_26_list[-1] and ema_12_list[-2] < ema_26_list[-2]:
            return 1
        return -1

    def get_buy_list(self, date):
        code_list = self.db_manager_wm.get_code_list()
        buy_list = list()
        for item in code_list:
            try:
                code = item["code"]
                price_list = list()
                expma_list = list()
                # 获取ema数据
                tk_details = self.db_manager_wm.find_by_key({"code": code})[0]
                for tk_item in [x for x in tk_details["price_list"] if x["close_price"] != 0]:
                    if time_cmp(str(date), tk_item["date_list"][-2]):
                        price_list.append(tk_item["close_price"])
                ema_12_list, ema_26_list = self.get_w_expma_2(price_list[:])
                if self.get_result(ema_12_list, ema_26_list) == 1:
                    buy_list.append(code)
            except Exception as e:
                continue
        return buy_list

    # 将策略结果同步到redis
    def update_redis(self, date):
        buy_list = self.get_buy_list(date)
        rm = RedisManager()
        rm.set_data("ema_" + str(date), buy_list)

    # 计算当前时间段ema值
    def get_w_expma(self, price_list):
        ema_12_list = list()
        for index in range(len(price_list)):
            if index == 0:
                ema_12_list.append(price_list[0])
            else:
                ema_12_list.append(round(ema_12_list[index - 1] * 11 / 13 + price_list[index] * 2 / 13, 4))
        ema_26_list = list()
        for index in range(len(price_list)):
            if index == 0:
                ema_26_list.append(price_list[0])
            else:
                ema_26_list.append(round(ema_26_list[index - 1] * 25 / 27 + price_list[index] * 2 / 27, 4))
        return ema_12_list, ema_26_list

    # 计算当前时间段ema值
    def get_w_expma_2(self, price_list):
        ema_12_list = list()
        for index in range(len(price_list)):
            if index == 0:
                ema_12_list.append(price_list[0])
            else:
                ema_12_list.append(round(ema_12_list[index - 1] * 4 / 6 + price_list[index] * 2 / 6, 4))
        ema_26_list = list()
        for index in range(len(price_list)):
            if index == 0:
                ema_26_list.append(price_list[0])
            else:
                ema_26_list.append(round(ema_26_list[index - 1] * 11 / 13 + price_list[index] * 2 / 13, 4))
        return ema_12_list, ema_26_list


if __name__ == "__main__":
    ste = TsStrategyExpma()
    for item in date_range("2018-01-01", str(datetime.datetime.now().date())):
        ste.update_redis(item)