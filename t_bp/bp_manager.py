#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '启动回测'
__author__ = 'JN Zhang'
__mtime__ = '2018/4/3'
"""
import datetime
import json

import numpy as np
from core.c_strategy.strategy_3 import TsStrategy3
from mongo_db.mongodb_manager import DBManager
from t_bp.file_utils import FileUtils

capital_base = 1000000
current_position = list()
history_capital = list()
history_order = list()
k_rate = 0.03
d_rate = -0.03


def get_cur_values(code, date, key):
    result = [x[key] for x in db_manager_tk.find_by_key({'code': code})[0]["price_list"] if x["cur_timer"] == date]
    if result:
        return round(float(result[0]), 2)
    return 0


def date_range(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days + 1
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]


def fun_buy(buy_list, date):
    global capital_base
    f_utils.insert_line("date->" + date)
    p_stage = capital_base / len(buy_list)  # 对资金池进行均分
    for code in buy_list:
        open_price = get_cur_values(code, date, "cur_open_price")
        if open_price != 0 and not np.isnan(open_price):
            amount = int(p_stage / open_price / 100) * 100
            if amount >= 100:
                item_position = [code, open_price, amount]
                current_position.append(item_position)
                # 保存开单记录
                f_utils.insert_line("buy-->" + json.dumps(item_position))


def fun_sell(date):
    global capital_base
    f_utils.insert_line("date->" + date)
    while current_position:
        item_position = current_position.pop()
        close_price = get_cur_values(item_position[0], date, "cur_close_price")
        if close_price != 0 and not np.isnan(close_price):
            profit = (close_price - item_position[1]) * item_position[2]
            capital_base += profit
            f_utils.insert_line("sell->" + json.dumps([item_position[0], profit, capital_base]))
    # 统计历史数据
    history_capital.append(capital_base)
    f_utils.insert_line("cash->" + capital_base)


def start_bp():
    st3 = TsStrategy3()
    history_capital.append(capital_base)
    # 初始化时间轴
    date_list = date_range("2018-03-05", "2018-04-13")
    for index in range(len(date_list)):
        cur_date = date_list[index]
        if datetime.datetime.strptime(cur_date, "%Y-%m-%d").weekday() == 0:
            buy_list = st3.get_buy_list(date_list[index-3])
            if buy_list:
                fun_buy(buy_list, cur_date)
        elif datetime.datetime.strptime(cur_date, "%Y-%m-%d").weekday() == 4:
            fun_sell(cur_date)
    net_rate = (history_capital[-1] - history_capital[0]) / history_capital[0]  # 计算回测结果
    print(round(net_rate * 100, 2), "%")


if __name__ == "__main__":
    f_utils = FileUtils("bp_result.txt", "a+")
    db_manager_tk = DBManager("tk_details")
    start_bp()
