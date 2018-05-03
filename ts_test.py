#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '测试用例'
__author__ = 'JN Zhang'
__mtime__ = '2018/5/3'
"""
from mongo_db.mongodb_manager import DBManager

if __name__ == "__main__":
    db_manager_wm = DBManager("wm_details")
    tk_details = db_manager_wm.find_by_key({"code": "601117.XSHG"})[0]["price_list"]
    for item in tk_details:
        print(item["frist_date"], item["close_price"])
