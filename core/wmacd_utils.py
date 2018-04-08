#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'wmacd计算工具'
__author__ = 'JN Zhang'
__mtime__ = '2018/4/6'
"""
import datetime


def date_range(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days + 1
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]


class WmacdUtils:
    def __init__(self):
        pass

    # 更新当前时间轴
    def update_w_time(self):
        cur_time = datetime.datetime.now().date()

    # 计算当前时间段的wmacd值
    def update_w_macd(self, price_list):
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


if __name__ == "__main__":
    print(date_range("2017-01-01", "2018-01-01"))
