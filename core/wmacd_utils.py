#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'wmacd计算工具'
__author__ = 'JN Zhang'
__mtime__ = '2018/4/6'
"""
import datetime

from mongo_db.mongodb_manager import DBManager


def date_range(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days + 1
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]


class WmacdUtils:
    def __init__(self):
        self.dm = DBManager("wm_details")

    # 更新当前时间轴
    def update_w_time(self, date_list=list()):
        if len(date_list) == 0:
            date_list = date_range("2016-01-01", str(datetime.datetime.now().date()))
        code_list = [x["code"][:6] for x in self.dm.find_by_id("")]
        tk_details0 = self.dm.find_by_id(code_list[0])
        cur_date_list = list()
        # 获取数据库中已经存在的日期列表
        for tk_item in tk_details0["wmacd_list"]:
            cur_date_list.extend(tk_item["cur_date"])
        for date_item in date_list:
            # 如果当前时间节点不存在数据库中则更新时间轴
            if date_item not in date_list:
                if datetime.datetime.strptime(date_item, "%Y-%m-%d").weekday() == 0:
                    # 如果当前日期是周一则新增一条记录
                    for tk_code in code_list:
                        wmacd_item = {
                            "cur_date": date_item,
                            "cur_open_price": 0,
                            "cur_max_price": 0,
                            "cur_min_price": 0,
                            "cur_close_price": 0,
                            "cur_price_range": 0,
                        }
                        self.dm.push_one({'code': tk_code}, {"wmacd_list": wmacd_item})
                # else:
                # self.dm.add_tk_item(key, price)
                # 更新时间节点的数据

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
    # print(date_range("2016-01-01", str(datetime.datetime.now().date())))
    print(datetime.datetime.strptime("2018-04-09", "%Y-%m-%d").weekday())
