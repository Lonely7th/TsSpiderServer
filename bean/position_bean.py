#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JN Zhang'
__mtime__ = '2018/8/8'
"""


class PositionBean(object):
    def __init__(self, ticker, price, amount, date):
        self.ticker = ticker
        self.price = price
        self.amount = amount
        self.date = date

    @property
    def ticker(self):
        return self._ticker

    @property
    def price(self):
        return float(self._price)

    @property
    def amount(self):
        return int(self._amount)

    @property
    def date(self):
        return self._date

    @ticker.setter
    def ticker(self, value):
        self._ticker = value

    @price.setter
    def price(self, value):
        self._price = value

    @amount.setter
    def amount(self, value):
        self._amount = value

    @date.setter
    def date(self, value):
        self._date = value
