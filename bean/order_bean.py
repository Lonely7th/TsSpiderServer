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

    @property
    def date(self):
        return self._date

    @property
    def ticker(self):
        return self._ticker

    @property
    def amount(self):
        return int(self._amount)

    @date.setter
    def date(self, value):
        self._date = value

    @ticker.setter
    def ticker(self, value):
        self._ticker = value

    @amount.setter
    def amount(self, value):
        self._amount = value
