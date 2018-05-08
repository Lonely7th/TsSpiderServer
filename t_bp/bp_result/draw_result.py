#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '绘图工具'
__author__ = 'JN Zhang'
__mtime__ = '2018/4/24'
"""
import numpy as np
import matplotlib.pyplot as plt
import os


base_path = os.path.abspath(os.path.join(os.getcwd(), "../..")) + "/t_bp/bp_result/"


def draw_profit(file):
    profit_list = list()
    while True:
        line = file.readline()
        if "" == line:
            break
        if "cash->" in line:
            profit_list.append(round(float(line[6:]), 2))
    plt.subplot(111)
    lable_x = np.arange(len(profit_list))
    plt.plot(lable_x, profit_list, color="r", linewidth=1.0, linestyle="-")
    plt.xlim(lable_x.min(), lable_x.max() * 1.1)
    plt.ylim(min(profit_list) * 0.9, max(profit_list) * 1.1)
    plt.grid(True)
    plt.show()


def draw_profit_bar(file):
    profit_list = list()
    while True:
        line = file.readline()
        if "" == line:
            break
        if "sell->" in line:
            profit_list.append(float(line[6:].split(",")[1][2:-2]))
    plt.subplot(111)
    lable_x = np.arange(len(profit_list))
    lable_y = [x * 0 for x in range(len(profit_list))]
    # 绘制中轴线
    plt.plot(lable_x, lable_y, color="#404040", linewidth=1.0, linestyle="-")
    profit_list_h = [x for x in profit_list if x >= 0]
    profit_list_l = [x for x in profit_list if x < 0]
    plt.bar(lable_x, profit_list, color="g", width=1.0)
    plt.xlim(lable_x.min(), lable_x.max() * 1.1)
    plt.ylim(min(profit_list), max(profit_list) * 1.1)
    plt.grid(True)
    plt.show()
    print(max(profit_list_h), min(profit_list_l))


def draw_w_profit_bar(file):
    profit_list = list()
    while True:
        line = file.readline()
        if "" == line:
            break
        if "cash->" in line:
            profit_list.append(round(float(line[6:]), 2))
    print(profit_list)
    profit_net_list = list()
    for index in range(1, len(profit_list)):
        profit_net_list.append((profit_list[index] - profit_list[index-1]) / profit_list[index-1])
    print(profit_net_list)
    print(len([x for x in profit_net_list if x > 0]))
    print(len([x for x in profit_net_list if x < 0]))
    plt.subplot(111)
    lable_x = np.arange(len(profit_net_list))
    lable_y = [x * 0 for x in range(len(profit_net_list))]
    # 绘制中轴线
    plt.plot(lable_x, lable_y, color="#404040", linewidth=1.0, linestyle="-")
    plt.bar(lable_x, profit_net_list, color="r", width=0.8)
    plt.xlim(lable_x.min(), lable_x.max() * 1.1)
    plt.ylim(min(profit_net_list) * 1.1, max(profit_net_list) * 1.1)
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    __file = open(base_path + "bp_result1_2.txt", "r")
    # draw_profit(__file)
    # draw_profit_bar(__file)
    draw_w_profit_bar(__file)
