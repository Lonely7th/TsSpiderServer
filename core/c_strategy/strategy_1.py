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


def fun_decision(data):
    print(data)


def profit_expectation(index, price_list, period=7):
    cur_profit = 0
    if index + period < len(price_list):
        cur_profit = (price_list[index+period]-price_list[index]) / price_list[index]
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
