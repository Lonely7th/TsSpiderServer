#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '启动回测'
__author__ = 'JN Zhang'
__mtime__ = '2018/4/3'
"""
import datetime
import numpy as np
from core.c_strategy.strategy_3 import TsStrategy3

capital_base = 1000000
current_position = list()
history_capital = list()
history_order = list()
tk_list = list()
k_rate = 0.03
d_rate = -0.03
error_data = 76


def date_range(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days + 1
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]


def fun_buy(buy_list):
    global capital_base
    # 对资金池进行均分
    p_stage = capital_base / len(buy_list)
    for index in buy_list:
        # 获取开盘价(默认以每周一的开盘价开仓)
        open_price = tk_list[index].get_open_list()
        if open_price and not np.isnan(open_price):
            amount = int(p_stage / open_price / 100) * 100
            if amount >= 100:
                capital_base -= amount * open_price
                current_position.append([index, open_price, amount])


def fun_sell():
    pass


def start_bp():
    st3 = TsStrategy3()
    # 初始化时间轴
    date_list = date_range("2016-01-04", "2018-12-30")
    for index in range(len(date_list)):
        cur_date = date_list[index]
        if datetime.datetime.strptime(cur_date, "%Y-%m-%d").weekday() == 0:
            buy_list = st3.get_buy_list(cur_date)
            if buy_list:
                fun_buy(buy_list)
        elif datetime.datetime.strptime(cur_date, "%Y-%m-%d").weekday() == 4:
            fun_sell()


if __name__ == "__main__":
    start_bp()
