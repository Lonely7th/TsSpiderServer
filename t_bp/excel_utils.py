#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JN Zhang'
__mtime__ = '2018/6/12'
"""
import json
from time import sleep

import xlrd
import requests


if __name__ == "__main__":
    data = xlrd.open_workbook("D:\location.xlsx")
    table = data.sheets()[0]
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    for i in range(1, nrows):
        rowValues = table.row_values(i)  # 某一行数据
        # 地理位置反编译
        url = "http://maps.google.cn/maps/api/geocode/json?latlng=" + str(rowValues[0]) + "," + str(rowValues[1]) + "&sensor=false&language=zh-CN"
        max_try = 8
        json_content = ""
        for tries in range(max_try):
            try:
                content = requests.get(url).content
                json_content = json.loads(content)["results"][0]["formatted_address"]
                break
            except Exception as e:
                if tries < (max_try - 1):
                    sleep(2)
                    continue
        print(rowValues[0], rowValues[1], json_content)
