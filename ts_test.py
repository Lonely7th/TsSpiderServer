#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '测试用例'
__author__ = 'JN Zhang'
__mtime__ = '2018/5/3'
"""
import time

import requests
from mongo_db.mongodb_manager import DBManager
import os
base_path = os.path.abspath(os.path.join(os.getcwd())) + "/t_bp/bp_result/"


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


if __name__ == "__main__":
    # db_manager_wm = DBManager("wm_details")
    # tk_details = db_manager_wm.find_by_key({"code": "601117.XSHG"})[0]["price_list"]
    # for item in tk_details:
    #     print(item["frist_date"], item["close_price"])
    fun_01()
