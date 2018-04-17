#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '交易策略03'
__author__ = 'JN Zhang'
__mtime__ = '2018/4/6'
"""
import datetime
import numpy as np

from bean.tk_wmacd_bean import tkWMacdBean
from mongo_db.mongodb_manager import DBManager
from t_redis.redis_manager import RedisManager


def cmp_datatime(item):
    return datetime.datetime.strptime(item["cur_timer"], "%Y-%m-%d")


class TsStrategy3:
    def __init__(self):
        pass

    def get_result(self, ticker):
        if isinstance(ticker, tkWMacdBean) and len(ticker.get_wmacd_list()) > 30:
            if ticker.get_wmacd_list()[-1] > 0 >= ticker.get_wmacd_list()[-2]:
                if 0.1 > ticker.get_diff_list()[-1] > 0:
                    if np.mean(ticker.get_tur_list()[-5:-1]) < ticker.get_tur_list()[-1]:
                        return 1
        return -1

    # 将策略结果同步到redis
    def update_redis(self, date):
        db_manager_wm = DBManager("wm_details")
        code_list = db_manager_wm.find_by_id("")
        __result = list()
        for item in code_list:
            try:
                code = item["code"]
                # 获取wmacd数据
                ticker_list = list(db_manager_wm.find_by_id(tk_code=code))
                for tk_item in ticker_list:
                    if datetime.datetime.strptime(tk_item["cur_date"], "%Y-%m-%d") > datetime.datetime.strptime(date, "%Y-%m-%d"):
                        ticker_list.remove(tk_item)
                # 匹配日期
                ticker_list_sorted = sorted(ticker_list, key=lambda x: cmp_datatime(x), reverse=True)
                __ticker = tkWMacdBean(code,
                    [x["price_list"] for x in ticker_list_sorted],
                    [x["wmacd_list"] for x in ticker_list_sorted],
                    [x["diff_list"] for x in ticker_list_sorted],
                    [x["dea_list"] for x in ticker_list_sorted],
                    [x["tur_list"] for x in ticker_list_sorted],
                    [x["highest_list"] for x in ticker_list_sorted],
                    [x["open_list"] for x in ticker_list_sorted])
                if self.get_result(__ticker):
                    __result.append(code)
            except Exception:
                continue
        rm = RedisManager()
        rm.set_data(date, __result)


if __name__ == "__main__":
    st3 = TsStrategy3()
    st3.update_redis("2018-04-01")
