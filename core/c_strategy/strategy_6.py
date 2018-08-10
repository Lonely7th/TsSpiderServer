#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JN Zhang'
__mtime__ = '2018/8/10'
"""
import datetime

import numpy as np

from bean.tk_wmacd_bean import tkWMacdBean
from mongo_db.mongodb_manager import DBManager


def time_cmp(first_time, second_time):
    return datetime.datetime.strptime(first_time, "%Y-%m-%d") >= datetime.datetime.strptime(second_time, "%Y-%m-%d")


class TsStrategy6(object):
    def __init__(self):
        self.db_manager_wm = DBManager("fcr_w_details")

    # 排除一些虚假信号
    def get_result2(self, ticker):
        if isinstance(ticker, tkWMacdBean) and len(ticker.get_wmacd_list()) > 30:
            if 0 > ticker.get_wmacd_list()[-1] > ticker.get_wmacd_list()[-2] > ticker.get_wmacd_list()[-3]:
                if 0 > ticker.get_diff_list()[-1] > -0.1:
                    if np.mean(ticker.get_tur_list()[-5:-1]) < ticker.get_tur_list()[-1]:
                        if ticker.get_wmacd_list()[-3] < 0 and ticker.get_wmacd_list()[-4] < 0 and ticker.get_wmacd_list()[-5] < 0:
                            return 1
        return -1

    def get_buy_list(self, date):
        code_list = self.db_manager_wm.get_code_list()
        buy_list = list()
        for item in code_list:
            try:
                code = item["code"]
                price_list = list()
                tur_list = list()
                highest_list = list()
                open_list = list()
                date_list = list()
                # 获取wmacd数据
                tk_details = self.db_manager_wm.find_by_key({"code": code})[0]
                for tk_item in [x for x in tk_details["price_list"] if x["close"] != 0]:
                    if time_cmp(str(date), tk_item["date"]):
                        date_list.append(tk_item["date"])
                        price_list.append(float(tk_item["close"]))
                        tur_list.append(float(tk_item["volume"]))
                        highest_list.append(float(tk_item["high"]))
                        open_list.append(float(tk_item["open"]))
                wmacd_list, diff_list, dea_list = self.get_w_macd(price_list[:])
                # 创建wmacd实体
                tk_bean = tkWMacdBean(code, price_list, wmacd_list, diff_list, dea_list, tur_list, highest_list,
                                      open_list)
                if self.get_result2(tk_bean) == 1:
                    buy_list.append(code)
            except Exception as e:
                continue
        return buy_list

    # 计算当前时间段的wmacd值
    def get_w_macd(self, price_list):
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
        diff_list = list()
        for index in range(len(ema_12_list)):
            diff = ema_12_list[index] - ema_26_list[index]
            diff_list.append(diff)
        dea_list = list()
        for index in range(len(diff_list)):
            if index == 0:
                dea_list.append(diff_list[0])
            else:
                dea_list.append(round(dea_list[index - 1] * 0.8 + diff_list[index] * 0.2, 4))
        wmacd_list = list()
        for index in range(len(dea_list)):
            bar = (diff_list[index] - dea_list[index]) * 3
            wmacd_list.append(bar)
        return wmacd_list, diff_list, dea_list
