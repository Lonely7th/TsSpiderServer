#!/usr/bin/env python
# -*-coding:utf-8-*-
import requests
import pandas as pd
import numpy as np


def load_data(code):
    url = "http://47.95.243.173/tkdata?code=" + code
    req = requests.get(url).json()
    data_list = [eval(x) for x in req["data"][1:-1].replace("}, {", "}#{").split("#")]
    data_df = pd.DataFrame(data_list)
    return data_df


def fun_decision(data):
    print(data["cur_close_price"])


def profit_expectation():
    pass


if __name__ == "__main__":
    tk_dict = load_data("000001")
    fun_decision(tk_dict)
