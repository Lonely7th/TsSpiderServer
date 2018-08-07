#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '账户实体'
__author__ = 'JN Zhang'
__mtime__ = '2018/8/7'
"""
from bean.order_bean import OrderBean


class AccountBean(object):
    def __init__(self, capital_base):
        self.capital_base = capital_base  # 初始资金
        self.capital_available = self.capital_base  # 当前可用
        self.position_list = list()  # 当前持仓
        self.history_order_list = list()

    def fun_buy(self, order):
        if isinstance(order, OrderBean):
            pass

    def fun_sell(self, order):
        pass