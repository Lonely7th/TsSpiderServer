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
        buy_list = list()
        for item in code_list:
            try:
                code = item["code"]
                # 获取wmacd数据
                price_list = list(reversed([float(x) for x in line.split("#")[0].strip()[13:-2].split(",")]))
                tur_list = list(reversed([float(x) for x in line.split("#")[1].strip()[1:-2].split(",")]))
                highest_list = list(reversed([float(x) for x in line.split("#")[2].strip()[1:-2].split(",")]))
                open_list = list(reversed([float(x) for x in line.split("#")[3].strip()[1:-2].split(",")]))
                wmacd_list, diff_list, dea_list = fun_02(price_list[:])
                tk_bean = tkWMacdBean(line[:11], price_list, wmacd_list, diff_list, dea_list, tur_list, highest_list, open_list)
                if self.get_result(tk_bean):
                    buy_list.append(code)
            except Exception:
                continue
        rm = RedisManager()
        rm.set_data("wm_" + str(date), buy_list)


if __name__ == "__main__":
    st3 = TsStrategy3()
    st3.update_redis("2018-04-01")
