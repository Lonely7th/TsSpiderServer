#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JN Zhang'
__mtime__ = '2018/8/7'
"""
import datetime

from bean.order_bean import OrderBean
from bean.position_bean import PositionBean
from mongo_db.mongodb_manager import DBManager


class AccountBean(object):
    def __init__(self, capital_base=1000000):
        self.capital_base = capital_base  # 起始资金
        self.capital_available = capital_base  # 可用资金
        self.position_list = list()  # 当前持仓
        self.history_order_list = list()  # 订单记录
        self.db_manager_tk = DBManager("fcr_details")

    def fun_buy(self, order):
        if isinstance(order, OrderBean):
            open_price = self.get_cur_values(order.ticker, order.date, "open")
            if open_price <= 0 or open_price * order.amount > self.capital_available or self.get_cur_weekday(order.date) >= 5:
                return
            if self.get_position_by_ticker(order.ticker):  # 加仓
                item_position = self.get_position_by_ticker(order.ticker)
                surplus_value = ((item_position.price * item_position.amount) + (open_price * order.amount)) / (item_position.amount + order.amount)
                item_position.price = surplus_value  # 修改剩余价值
                item_position.amount = order.amount + item_position.amount
                self.capital_available -= open_price * order.amount
            else:  # 开仓
                item_position = PositionBean(order.ticker, open_price, order.amount, order.date)
                self.position_list.append(item_position)
                self.capital_available -= open_price * order.amount
            self.history_order_list.append(order)

    def fun_sell(self, order):
        if isinstance(order, OrderBean):
            item_position = self.get_position_by_ticker(order.ticker)
            if self.get_cur_weekday(order.date) < 5 and item_position:
                close_price = self.get_cur_values(order.ticker, order.date, "close")
                if self.get_date_diff(item_position.date, order.date) > 0 and close_price > 0:
                    if order.amount < item_position.amount:  # 减仓
                        surplus_value = ((item_position.price * item_position.amount) - (close_price * order.amount)) / (item_position.amount - order.amount)
                        item_position.price = surplus_value  # 修改剩余价值
                        item_position.amount = item_position.amount - order.amount  # 修改剩余持仓
                        self.capital_available += close_price * order.amount
                    else:  # 平仓
                        print(self.capital_available)
                        self.capital_available += close_price * item_position.amount
                        print(self.capital_available, close_price, item_position.price)
                        self.position_list.remove(item_position)

    def get_totla_capital(self):
        totla_capital = self.capital_available
        for position in self.position_list:
            totla_capital += position.price * position.amount
        return totla_capital

    def get_position_by_ticker(self, ticker):
        for item in self.position_list:
            if isinstance(item, PositionBean) and item.ticker == ticker:
                return item
        return []

    def get_cur_values(self, code, date, key):
        result = [x[key] for x in self.db_manager_tk.find_by_key({'code': code})[0]["price_list"] if x["date"] == date]
        if result:
            return round(float(result[0]), 2)
        return 0

    def get_cur_weekday(self, date):
        return datetime.datetime.strptime(date, "%Y-%m-%d").weekday()

    def get_date_diff(self, start, end, format="%Y-%m-%d"):
        strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
        days = (strptime(end, format) - strptime(start, format)).days
        return int(days)

    @property
    def capital_base(self):
        return self._capital_base

    @property
    def capital_available(self):
        return self._capital_available

    @property
    def position_list(self):
        return self._position_list

    @property
    def history_order_list(self):
        return self._history_order_list

    @capital_base.setter
    def capital_base(self, value):
        self._capital_base = value

    @capital_available.setter
    def capital_available(self, value):
        self._capital_available = value

    @position_list.setter
    def position_list(self, value):
        self._position_list = value

    @history_order_list.setter
    def history_order_list(self, value):
        self._history_order_list = value
