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
        self.db_manager_wm = DBManager("wm_details")
        self.db_manager_tk = DBManager("tk_details")

    # 初始化wmacd数据
    def init_w_time(self, code, date_list):
        # tk_details = self.dm.find_by_key({"code": code, "cur_timer": {"$in": cur_date_list}})
        tk_details = self.db_manager_tk.find_by_key({"code": code})
        for index in range(len(date_list)):
            if datetime.datetime.strptime(date_list[index], "%Y-%m-%d").weekday() == 0:
                cur_date_list = date_list[index: index+7]
                # 从数据库中获取这个时间段内的数据
                cur_tk_details = [x for x in tk_details["price_list"] if x["cur_timer"] in cur_date_list]
                open_price_list = [x["cur_open_price"] for x in cur_tk_details]
                max_price_list = [x["cur_max_price"] for x in cur_tk_details]
                min_price_list = [x["cur_min_price"] for x in cur_tk_details]
                close_price_list = [x["cur_close_price"] for x in cur_tk_details]
                total_volume_list = [x["cur_total_volume"] for x in cur_tk_details]
                total_money_list = [x["cur_total_money"] for x in cur_tk_details]
                wmacd_item = {
                    "date_list": cur_date_list,
                    "open_price": open_price_list[0],
                    "max_price": max(max_price_list),
                    "min_price": min(min_price_list),
                    "close_price": close_price_list[-1],
                    "total_volume": sum(total_volume_list),
                    "total_money": sum(total_money_list),
                }
                # 在数据库中添加一条记录
                self.db_manager_wm.add_tk_item(code, wmacd_item)
                index += 7
                print(wmacd_item)

    def update_w_macd(self):
        code_list = self.db_manager_wm.find_by_id("")
        for item in code_list:
            pass

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


if __name__ == "__main__":
    # 初始化时间轴
    date_list = date_range("2016-01-04", "2018-12-30")
    wu = WmacdUtils()
    wu.init_w_time("000001", date_list)
