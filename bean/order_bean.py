#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '订单实体'
__author__ = 'JN Zhang'
__mtime__ = '2018/8/7'
"""


class OrderBean(object):
    def __init__(self, date, ticker, amount):
        self.date = date
        self.ticker = ticker
        self.amount = amount

    def get_date(self):
        return self.date

    def get_ticker(self):
        return self.ticker

    def get_amount(self):
        return self.amount
