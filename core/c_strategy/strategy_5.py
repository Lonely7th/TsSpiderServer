#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JN Zhang'
__mtime__ = '2018/8/1'
"""
import datetime
import numpy as np

from bean.account_bean import AccountBean
from bean.order_bean import OrderBean
from core.c_strategy.strategy_3 import TsStrategy3
from core.c_strategy.strategy_3_f import TsStrategy3f
from core.c_strategy.strategy_5_f import TsStrategy5f
from mongo_db.mongodb_manager import DBManager


def date_range(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days + 1
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]


def get_cur_values(code, date, key):
    result = [x[key] for x in db_manager_tk.find_by_key({'code': code})[0]["price_list"] if x["date"] == date]
    if result:
        return round(float(result[0]), 2)
    return 0


if __name__ == "__main__":
    st5 = TsStrategy5f()
    db_manager_tk = DBManager("fcr_details")
    account = AccountBean()
    date_list = date_range("2018-01-01", "2018-07-31")
    for date in date_list:
        if datetime.datetime.strptime(date, "%Y-%m-%d").weekday() == 0:
            buy_list = st5.get_buy_list(date)
            if buy_list:
                p_stage = account.capital_available / len(buy_list)  # 对资金池进行均分
                for code in buy_list:
                    open_price = get_cur_values(code, date, "open")
                    if open_price != 0 and not np.isnan(open_price):
                        amount = int(p_stage / open_price / 100) * 100
                        if amount >= 100:
                            account.fun_buy(OrderBean(date, code, amount))
        if datetime.datetime.strptime(date, "%Y-%m-%d").weekday() == 4:
            for position in account.position_list[:]:
                account.fun_sell(OrderBean(date, position.ticker, position.amount))
        print(date, [x.ticker for x in account.position_list])
    net_rate = (account.get_totla_capital() - account.capital_base) / account.capital_base  # 计算回测结果
    print(round(net_rate * 100, 2), "%")
