#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JN Zhang'
__mtime__ = '2018/9/25'
"""
from mongo_db.mongodb_manager import DBManager
import matplotlib.pyplot as plt
import numpy as np

rate_fall = 0.7  # 下跌幅度
period = 30  # 计算周期
expect = 30  # 计算期望的周期


def draw_profit_bar(list1, list2):
    plt.subplot(111)
    lable_x = np.arange(len(list1))
    lable_y = [x * 0 for x in range(len(list1))]
    # 绘制中轴线
    plt.plot(lable_x, lable_y, color="#404040", linewidth=1.0, linestyle="-")
    plt.bar(lable_x, list1, color="r", width=1.0)
    plt.bar(lable_x, list2, color="g", width=1.0)
    plt.xlim(lable_x.min(), lable_x.max() * 1.1)
    plt.ylim(min(list2) * 1.1, max(list1) * 1.1)
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # 获取数据
    db_manager_wm = DBManager("fcr_details")
    code_list = db_manager_wm.get_code_list()
    result_list = list()
    for item in code_list:
        code = item["code"]
        print(code)
        tk_data = db_manager_wm.find_by_key({"code": code})[0]
        colse_list = [float(x["close"]) for x in tk_data["price_list"] if x["close"] != 0]
        len_list = len(colse_list)
        if colse_list:
            # 执行判断逻辑
            for index in range(expect, len(colse_list)):
                rate_1 = (colse_list[index-period] - colse_list[index]) / colse_list[index-period]  # 下跌幅度
                if rate_1 > rate_fall and len_list > index+expect:
                    exp_top = max(colse_list[index+1: index+expect])
                    exp_low = min(colse_list[index+1: index+expect])
                    rate_2 = (exp_top - colse_list[index]) / colse_list[index]
                    rate_3 = (exp_low - colse_list[index]) / colse_list[index]
                    result_list.append({"rate_1": rate_1, "rate_2": rate_2, "rate_3": rate_3})
    # 统计结果
    # 绘图
    draw_profit_bar([x["rate_2"] for x in result_list], [x["rate_3"] for x in result_list])
