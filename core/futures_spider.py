#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JN Zhang'
__mtime__ = '2018/8/21'
"""

import json
from time import sleep

import requests
from mongo_db.mongodb_manager import DBManager

symbol_list = ["RB0/螺纹钢","AG0/白银","AU0/黄金","CU0/沪铜","AL0/沪铝","ZN0/沪锌","PB0/沪铅","RU0/橡胶","FU0/燃油","WR0/线材","A0/大豆","M0/豆|粕","Y0/豆油","J0/焦炭","C0/玉米","L0/乙烯","P0/棕油","v0/PVC","RS0/菜籽","RM0/妄粥","FG0/玻璃","CF0/棉花","WS0/强麦","ER0/籼稻","ME0/甲醇","RO0/菜油","TA0/甲酸"]


class FuturesSpider:
    def __init__(self):
        self.dm = DBManager("futures_d_table")

    def init_table(self):
        for item in symbol_list:
            self.dm.add_one({"code": item.split("/")[0], "symbol": item.split("/")[1], "details": []})

    def start_crawl(self):
        for symbol in symbol_list:
            url = "http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesDailyKLine?symbol=" + symbol.split("/")[0]
            print(url)
            # 请求失败后重新请求(最多8次)
            max_try = 8
            for tries in range(max_try):
                try:
                    content = requests.get(url)
                    self.parse_pager(content.content, symbol.split("/")[0])
                    break
                except Exception:
                    if tries < (max_try - 1):
                        sleep(2)
                        continue
                    else:
                        print(symbol, "fail")

    def parse_pager(self, content, code):
        timer_list = [x["date"] for x in self.dm.find_one_by_key({"code": code})["details"]]
        data = json.loads(content)
        for item in data:
            __dict = {
                "date": item[0],
                "open": item[1],
                "high": item[2],
                "low": item[3],
                "close": item[4],
                "count": item[5]
            }
            if __dict["date"] not in timer_list:
                self.dm.add_futures_item(code, __dict)
        print(code, "success")


if __name__ == '__main__':
    fs = FuturesSpider()
    fs.init_table()
    fs.start_crawl()
