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
capital_available = capital_base
current_position = list()
history_capital = list()
history_order = list()
k_rate = 0.05
d_rate = -0.05


def get_cur_values(code, date, key):
    result = [x[key] for x in db_manager_tk.find_by_key({'code': code})[0]["price_list"] if x["date"] == date]
    if result:
        return round(float(result[0]), 2)
    return 0


def date_range(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days + 1
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]


# 时间差
def date_diff(start, end, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days
    return int(days)


# 计算当前资金总量
def get_all_capital():
    current_capital = capital_base
    for item_position in current_position[:]:
        current_capital += item_position[1] * item_position[2]
    return current_capital


def fun_buy(buy_list, date):
    global capital_base
    f_utils.insert_line("date->" + date)
    p_stage = capital_base / len(buy_list)  # 对资金池进行均分
    for code in buy_list:
        open_price = get_cur_values(code, date, "open")
        if open_price != 0 and not np.isnan(open_price):
            amount = int(p_stage / open_price / 100) * 100
            if amount >= 100:
                item_position = [code, open_price, amount, date]
                current_position.append(item_position)
                capital_base -= open_price * amount
                # 保存开单记录
                f_utils.insert_line("buy-->" + json.dumps(item_position))


def fun_sell(date):
    global capital_base
    for item_position in current_position[:]:
        close_price = get_cur_values(item_position[0], date, "close")
        if close_price != 0:
            profit_rate = (close_price - item_position[1]) / item_position[1]  # 计算收益率
            if datetime.datetime.strptime(date, "%Y-%m-%d").weekday() == 4:
                capital_base += close_price * item_position[2]
                f_utils.insert_line(
                    "sell->" + json.dumps([item_position[0], str(round(profit_rate * 100, 2)) + "%", capital_base, date]))
                current_position.remove(item_position)
    # 统计历史数据
    history_capital.append(capital_base)
    f_utils.insert_line("cash->" + str(get_all_capital()))


def fun_sell_2(date):
    global capital_base
    cur_weekday = datetime.datetime.strptime(date, "%Y-%m-%d").weekday()
    if cur_weekday in range(1, 5):
        f_utils.insert_line("date->" + date)
        for item_position in current_position[:]:
            close_price = get_cur_values(item_position[0], date, "close")
            if close_price != 0 and not np.isnan(close_price):
                profit_rate = (close_price - item_position[1]) / item_position[1]  # 计算收益率
                if date_diff(item_position[-1], date) > 0 and profit_rate < d_rate and item_position in current_position:  # 跌破平仓线后
                    capital_base += close_price * item_position[2]
                    f_utils.insert_line("sell->" + json.dumps([item_position[0], str(round(profit_rate * 100, 2)) + "%", capital_base]))
                    current_position.remove(item_position)
                if date_diff(item_position[-1], date) > 0 and item_position in current_position:
                    if close_price > item_position[1]:
                        expect_price = item_position[1] * ((1 + k_rate) ** date_diff(item_position[-1], date))  # 价格的期望值
                        if expect_price > close_price:
                            capital_base += close_price * item_position[2]
                            f_utils.insert_line("sell->" + json.dumps([item_position[0], str(round(profit_rate * 100, 2)) + "%", capital_base]))
                            current_position.remove(item_position)

        # 统计历史数据
        history_capital.append(capital_base)
        f_utils.insert_line("cash->" + str(get_all_capital()))


def fun_sell_3(date):
    global capital_base
    cur_weekday = datetime.datetime.strptime(date, "%Y-%m-%d").weekday()
    if cur_weekday in range(1, 5):
        f_utils.insert_line("date->" + date)
        for item_position in current_position[:]:
            close_price = get_cur_values(item_position[0], date, "cur_close_price")
            if close_price != 0 and not np.isnan(close_price):
                profit_rate = (close_price - item_position[1]) / item_position[1]  # 计算收益率
                if cur_weekday == 4 or profit_rate >= k_rate:
                    capital_base += close_price * item_position[2]
                    f_utils.insert_line("sell->" + json.dumps([item_position[0], str(round(profit_rate * 100, 2)) + "%", capital_base]))
                    current_position.remove(item_position)
        # 统计历史数据
        history_capital.append(capital_base)
        f_utils.insert_line("cash->" + str(get_all_capital()))


def start_bp():
    st3 = TsStrategy3()
    history_capital.append(capital_base)
    # 初始化时间轴
    date_list = date_range("2017-06-05", "2017-12-31")
    for index in range(len(date_list)):
        cur_date = date_list[index]
        print(cur_date)
        fun_sell(cur_date)
        if datetime.datetime.strptime(cur_date, "%Y-%m-%d").weekday() == 0:
            buy_list = st3.get_buy_list(cur_date)
            if buy_list:
                fun_buy(buy_list, cur_date)
    net_rate = (history_capital[-1] - history_capital[0]) / history_capital[0]  # 计算回测结果
    print(round(net_rate * 100, 2), "%")


if __name__ == "__main__":
    f_utils = FileUtils("bp_result3_1.txt", "w")
    db_manager_tk = DBManager("fcr_details")
    start_bp()
