#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JN Zhang'
__mtime__ = '2018/6/8'
"""
import datetime
import numpy as np
import matplotlib.pyplot as plt
from mongo_db.mongodb_manager import DBManager


def time_cmp(first_time, second_time):
    return datetime.datetime.strptime(first_time, "%Y-%m-%d") >= datetime.datetime.strptime(second_time, "%Y-%m-%d")


class EmaManager:
    def __init__(self):
        self.db_manager_tk = DBManager("fcr_w_details")

    def get_buy_list(self, date):
        code_list = [x for x in self.db_manager_tk.get_code_list_02()]
        buy_list = list()
        for code_item in code_list:
            ticker = code_item["ticker"]
            # 获取数据
            close_list = list()
            tk_details = self.db_manager_tk.find_one_by_key({"ticker": ticker})
            for tk_item in [x for x in tk_details["price_list"]]:
                if time_cmp(str(date), tk_item["date"]):
                    close_list.append(float(tk_item["close"]))
            # 执行判断条件
            if len(close_list) > 20:
                ema_20_1 = np.mean(close_list[-20:])
                ema_20_2 = np.mean(close_list[-21:-1])
                if close_list[-1] > ema_20_1 and close_list[-2] < ema_20_2:
                    buy_list.append(ticker)
        return buy_list

    def get_sell_list(self, date):
        code_list = [x for x in self.db_manager_tk.get_code_list_02()]
        sell_list = list()
        for code_item in code_list:
            ticker = code_item["ticker"]
            # 获取数据
            close_list = list()
            tk_details = self.db_manager_tk.find_one_by_key({"ticker": ticker})
            for tk_item in [x for x in tk_details["price_list"]]:
                if time_cmp(str(date), tk_item["date"]):
                    close_list.append(float(tk_item["close"]))
            # 执行判断条件
            if len(close_list) > 20:
                ema_10_1 = np.mean(close_list[-10:])
                ema_10_2 = np.mean(close_list[-11:-1])
                if close_list[-1] < ema_10_1 and close_list[-2] > ema_10_2:
                    sell_list.append(ticker)
        return sell_list

    def fun_01(self):
        code_list = [x for x in self.db_manager_tk.get_code_list_02()]
        result_list = list()
        for code_item in code_list:
            ticker = code_item["ticker"]
            # 获取数据
            tk_details = self.db_manager_tk.find_one_by_key({"ticker": ticker})
            close_list = list()
            open_list = list()
            high_list = list()
            low_list = list()
            volume_list = list()
            for x in tk_details["price_list"]:
                if x["close"] != "":
                    close_list.append(float(x["close"]))
                    open_list.append(float(x["open"]))
                    high_list.append(float(x["high"]))
                    low_list.append(float(x["low"]))
                    volume_list.append(float(x["volume"]))
            ema_list = list()
            for i in range(len(close_list)):
                if i >= 20:
                    ema_list.append(np.mean(close_list[i-20:i]))
                else:
                    ema_list.append(close_list[i])
            # 执行判断条件
            for date in range(len(close_list)-1):
                # 均线呈现向上趋势
                if ema_list[date] > ema_list[date - 4]:
                    # K线上穿且连续8周位于均线之下
                    if close_list[date] > ema_list[date]:
                        if close_list[date-1] < ema_list[date-1] and close_list[date-2] < ema_list[date-2] and close_list[date-3] < ema_list[date-3] and close_list[date - 4] < ema_list[date - 4]:
                            profit_rate = (close_list[date + 1] - open_list[date + 1]) / open_list[date + 1]
                            result_list.append(profit_rate)
        print(len(result_list))
        result_list_up = [x for x in result_list if x > 0]
        result_list_down = [x for x in result_list if x < 0]
        print(len(result_list_up), max(result_list_up), np.mean(result_list_up))
        print(len(result_list_down), min(result_list_down), np.mean(result_list_down))
        # 绘图
        plt.subplot(111)
        lable_x = np.arange(len(result_list))
        lable_y = [x * 0 for x in range(len(result_list))]
        # 绘制中轴线
        plt.plot(lable_x, lable_y, color="#404040", linewidth=1.0, linestyle="-")
        plt.bar(lable_x, result_list, color="g", width=1.0)
        plt.xlim(lable_x.min(), lable_x.max() * 1.1)
        plt.ylim(min(result_list) * 1.1, max(result_list) * 1.1)
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    code_m = EmaManager()
    code_m.fun_01()
    # print(code_m.get_buy_list())
