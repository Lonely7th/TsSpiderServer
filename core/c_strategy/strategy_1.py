#!/usr/bin/env python
# -*-coding:utf-8-*-
import requests
import pandas as pd
import numpy as np
import os


def load_data(code):
    url = "http://47.95.243.173/tkdata?code=" + code
    req = requests.get(url).json()
    data_list = list(reversed([eval(x) for x in req["data"][1:-1].replace("}, {", "}#{").split("#")]))
    data_df = pd.DataFrame(data_list)
    return data_df


k1 = 0.2
k2 = 0.05


def fun_decision(data, period=180):
    close_price_list = data["cur_close_price"]
    result_list = list()
    if len(close_price_list) > period:
        for index in range(period, len(close_price_list)):
            max_price = np.max(close_price_list[index - period: index])
            cur_price = close_price_list[index]
            if (max_price - cur_price) / cur_price > k1:
                result_list.append(profit_expectation(index, close_price_list))
    print(len([x for x in result_list if x > 0]))
    print(len([x for x in result_list if x <= 0]))


def profit_expectation(index, price_list, period=7):
    cur_profit = 0
    if index + period < len(price_list):
        cur_profit = (price_list[index + period] - price_list[index]) / price_list[index]
    return cur_profit


if __name__ == "__main__":
    file_path = os.path.abspath(os.path.join(os.getcwd(), "../..")) + "/bean/data_code.txt"
    code_file = open(file_path, mode='r', encoding='utf-8')
    while True:
        line = code_file.readline()
        if '' == line:
            break
        str_code = line.split()[0][:6]
        fun_decision(load_data(str_code))
