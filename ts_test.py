#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '测试用例'
__author__ = 'JN Zhang'
__mtime__ = '2018/5/3'
"""
import datetime
import time

import requests
from mongo_db.mongodb_manager import DBManager
import os
base_path = os.path.abspath(os.path.join(os.getcwd())) + "/t_bp/bp_result/"


def time_cmp(first_time, second_time):
    return datetime.datetime.strptime(first_time, "%Y-%m-%d") >= datetime.datetime.strptime(second_time, "%Y-%m-%d")


def date_range(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days + 1
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]


def fun_01():
    file = open(base_path + "bp_result.txt", "r")
    while True:
        line = file.readline()
        if "" == line:
            break
        if "buy-->" in line:
            if "2018" in line[6:].split(",")[3][2:-3]:
                content = requests.get("http://47.95.243.173/wmdata?date=" + line[6:].split(",")[3][2:-3]).content
                print(content)
                if line[6:].split(",")[0][2:-1] not in str(content):
                    print(line[6:].split(",")[3][2:-3])
                time.sleep(1)


def fun_02():
    date_list = date_range("2017-05-04", "2018-05-21")
    for date in date_list:
        code = "000001.XSHE"
        price_list = list()
        tur_list = list()
        highest_list = list()
        open_list = list()
        # 获取wmacd数据
        db_manager_wm = DBManager("wm_details")
        tk_details = db_manager_wm.find_by_key({"code": code})[0]
        for tk_item in [x for x in tk_details["price_list"] if x["close_price"] != 0]:
            if time_cmp(str(date), tk_item["date_list"][-2]):
                price_list.append(tk_item["close_price"])
                tur_list.append(tk_item["total_volume"])
                highest_list.append(tk_item["max_price"])
                open_list.append(tk_item["open_price"])
        print(price_list, date)


if __name__ == "__main__":
    # db_manager_wm = DBManager("wm_details")
    # tk_details = db_manager_wm.find_by_key({"code": "601117.XSHG"})[0]["price_list"]
    # for item in tk_details:
    #     print(item["frist_date"], item["close_price"])
    fun_02()
