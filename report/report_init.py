#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '初始化数据'
__author__ = 'JN Zhang'
__mtime__ = '2018/9/25'
"""
import os
from time import sleep

import baostock as bs
from mongo_db.mongodb_manager import DBManager

base_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + "/bean"


def init_table():
    _file = open(base_path, "r", encoding="utf-8")
    while True:
        line = _file.readline()
        if '' == line:
            break
        str_code = line.split()[0]
        str_title = line.split()[1]
        if "XSHE" in str_code:
            ticker = "sz." + str_code[:6]
        elif "XSHG" in str_code:
            ticker = "sh." + str_code[:6]
        dm.add_one({"code": str_code, "ticker": ticker, "title": str_title, "price_list": []})


def start_crawl():
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)
    code_list = dm.get_code_list_02()
    for item in code_list:
        ticker = item["ticker"]
        max_try = 8
        for tries in range(max_try):
            rs = bs.query_history_k_data(ticker,
                                         "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg",
                                         start_date='2018-01-01', end_date='2018-07-28', frequency="d", adjustflag="2")
            if rs.error_code == '0':
                parse_pager(rs, ticker)
                break
            elif tries < (max_try - 1):
                sleep(2)
                continue
    bs.logout()


def parse_pager(content, ticker):
    timer_list = [x["date"] for x in dm.find_one_by_key({"ticker": ticker})["price_list"]]
    while content.next():
        item_row = content.get_row_data()
        __dict = {
            "date": item_row[0],
            "code": item_row[1],
            "open": item_row[2],
            "high": item_row[3],
            "low": item_row[4],
            "close": item_row[5],
            "preclose": item_row[6],
            "volume": item_row[7],
            "amount": item_row[8],
            "adjustflag": item_row[9],
            "turn": item_row[10],
            "tradestatus": item_row[11],
            "pctChg": item_row[12]
        }
        if __dict["date"] not in timer_list:
            dm.add_tk_item(ticker, __dict)
    print(ticker, "success")


if __name__ == "__main__":
    dm = DBManager("fcr_details")
    # 初始化数据库表结构
    init_table()
    # 填充数据
    start_crawl()
