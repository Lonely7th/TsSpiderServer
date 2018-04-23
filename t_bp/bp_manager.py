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
from mongo_db.mongodb_manager import DBManager

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


def fun_buy(buy_list, date):
    global capital_base
    p_stage = capital_base / len(buy_list)  # 对资金池进行均分
    for code in buy_list:
        open_price = round(db_manager_tk.find_by_key({"code": code, "price_list.cur_timer": date})[0]["cur_open_price"], 2)
        if open_price and not np.isnan(open_price):
            amount = int(p_stage / open_price / 100) * 100
            if amount >= 100:
                current_position.append([code, open_price, amount])


def fun_sell(date):
    global capital_base
    while current_position:
        item_position = current_position.pop()
        close_price = round(db_manager_tk.find_by_key({"code": item_position[0], "price_list.cur_timer": date})[0]["cur_close_price"], 2)
        capital_base += (close_price - item_position[1]) * item_position[2]
        # 统计历史数据
        history_capital.append(capital_base)


def start_bp():
    st3 = TsStrategy3()
    history_capital.append(capital_base)
    # 初始化时间轴
    date_list = date_range("2018-01-02", "2018-04-06")
    for index in range(len(date_list)):
        cur_date = date_list[index]
        if datetime.datetime.strptime(cur_date, "%Y-%m-%d").weekday() == 0:
            # 获取上周五的开仓列表
            buy_list = st3.get_buy_list(date_list[index-3])
            if buy_list:
                fun_buy(buy_list, cur_date)
        elif datetime.datetime.strptime(cur_date, "%Y-%m-%d").weekday() == 4:
            fun_sell(cur_date)
    net_rate = (history_capital[-1] - history_capital[0]) / history_capital[0]  # 计算回测结果
    print(round(net_rate * 100, 2), "%")


if __name__ == "__main__":
    db_manager_tk = DBManager("tk_details")
    start_bp()
