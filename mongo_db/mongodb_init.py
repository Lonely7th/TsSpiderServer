#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '初始化数据库(每次配置新环境时运行)'
__author__ = 'JN Zhang'
__mtime__ = '2018/2/28'
"""
import os

from mongo_db.mongodb_manager import DBManager

base_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + "/bean"

if __name__ == "__main__":
    dm = DBManager("wm_details")
    file_path = base_path + "/data_code.txt"
    _file = open(file_path, "r", encoding='utf-8')
    tk_list = list()
    while True:
        line = _file.readline()
        if '' == line:
            break
        str_code = line.split()[0]
        str_title = line.split()[1]
        dm.add_one({"code": str_code, "title": str_title, "price_list": []})
