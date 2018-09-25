#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JN Zhang'
__mtime__ = '2018/9/25'
"""
from mongo_db.mongodb_manager import DBManager

if __name__ == "__main__":
    # 获取数据
    db_manager_wm = DBManager("fcr_details")
    code_list = db_manager_wm.get_code_list()
    for item in code_list:
        code = item["code"]
        print(code)
        tk_data = db_manager_wm.find_by_key({"code": code})[0]
        tk_colse = [x["close"] for x in tk_data["price_list"] if x["close"] != 0]
        print(tk_colse)
    # 执行判断逻辑
    
    # 统计结果
    # 绘图
    pass
