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
    def init_w_time(self):
        # 初始化时间轴
        date_list = date_range("2016-01-04", "2018-12-30")
        # tk_details = self.dm.find_by_key({"code": code, "cur_timer": {"$in": cur_date_list}})
        ticker_list = self.db_manager_wm.get_code_list()
        for tk_item in ticker_list:
            code = tk_item["code"]
            print(code)
            tk_details = self.db_manager_tk.find_by_key({"code": code})[0]
            for index in range(len(date_list)):
                if datetime.datetime.strptime(date_list[index], "%Y-%m-%d").weekday() == 0:
                    cur_date_list = date_list[index: index+7]
                    # 从数据库中获取这个时间段内的数据
                    cur_tk_details = [x for x in tk_details["price_list"] if x["cur_timer"] in cur_date_list]
                    try:
                        open_price_list = [float(x["cur_open_price"]) for x in cur_tk_details]
                        max_price_list = [float(x["cur_max_price"]) for x in cur_tk_details]
                        min_price_list = [float(x["cur_min_price"]) for x in cur_tk_details]
                        close_price_list = [float(x["cur_close_price"]) for x in cur_tk_details]
                        total_volume_list = [int(x["cur_total_volume"].replace(",", "")) for x in cur_tk_details]
                        total_money_list = [int(x["cur_total_money"].replace(",", "")) for x in cur_tk_details]
                    except Exception as e:
                        continue
                    if cur_tk_details:
                        wmacd_item = {
                            "frist_date": cur_date_list[0],
                            "date_list": cur_date_list,
                            "open_price": open_price_list[0],
                            "max_price": max(max_price_list),
                            "min_price": min(min_price_list),
                            "close_price": close_price_list[-1],
                            "total_volume": sum(total_volume_list),
                            "total_money": sum(total_money_list),
                        }
                    else:
                        wmacd_item = {
                            "frist_date": cur_date_list[0],
                            "date_list": cur_date_list,
                            "open_price": 0,
                            "max_price": 0,
                            "min_price": 0,
                            "close_price": 0,
                            "total_volume": 0,
                            "total_money": 0,
                        }
                    # 在数据库中添加一条记录
                    self.db_manager_wm.add_tk_item(code, wmacd_item)

    def update_w_macd(self, cur_date=datetime.datetime.now().date()):
        date_list = date_range("2016-01-04", "2018-12-30")
        for index in range(len(date_list)):
            # 匹配到当前时间所在的区间
            if datetime.datetime.strptime(date_list[index], "%Y-%m-%d").weekday() == 0:
                cur_date_list = date_list[index: index + 7]
                if str(cur_date) in cur_date_list:
                    ticker_list = self.db_manager_wm.get_code_list()
                    # 更新每支股票的数据
                    for tk_item in ticker_list:
                        code = tk_item["code"]
                        tk_details = self.db_manager_tk.find_by_key({"code": code})[0]
                        # 从数据库中获取这个时间段内的数据
                        cur_tk_details = [x for x in tk_details["price_list"] if x["cur_timer"] in cur_date_list]
                        open_price_list = [float(x["cur_open_price"]) for x in cur_tk_details]
                        max_price_list = [float(x["cur_max_price"]) for x in cur_tk_details]
                        min_price_list = [float(x["cur_min_price"]) for x in cur_tk_details]
                        close_price_list = [float(x["cur_close_price"]) for x in cur_tk_details]
                        total_volume_list = [int(x["cur_total_volume"].replace(",", "")) for x in cur_tk_details]
                        total_money_list = [int(x["cur_total_money"].replace(",", "")) for x in cur_tk_details]
                        if cur_tk_details:
                            wmacd_item = {
                                "frist_date": cur_date_list[0],
                                "date_list": cur_date_list,
                                "open_price": open_price_list[0],
                                "max_price": max(max_price_list),
                                "min_price": min(min_price_list),
                                "close_price": close_price_list[-1],
                                "total_volume": sum(total_volume_list),
                                "total_money": sum(total_money_list),
                            }
                            # 修改数据库中的数据
                            self.db_manager_wm.update_wm_price_list(code, wmacd_item["frist_date"], wmacd_item)


if __name__ == "__main__":
    wu = WmacdUtils()
    wu.init_w_time()
    # wu.update_w_macd()
