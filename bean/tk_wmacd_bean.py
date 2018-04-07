#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JN Zhang'
__mtime__ = '2018/4/7'
"""


class tkWMacdBean(object):

    def get_code(self):
        return self.code

    def get_price_list(self):
        return self.price_list

    def set_price_list(self, price_list):
        self.price_list = price_list

    def get_wmacd_list(self):
        return self.wmacd_list

    def set_wmacd_list(self, wmacd_list):
        self.wmacd_list = wmacd_list

    def set_diff_list(self, diff_list):
        self.diff_list = diff_list

    def get_diff_list(self):
        return self.diff_list

    def get_dea_list(self):
        return self.dea_list

    def get_tur_list(self):
        return self.tur_list

    def set_tur_list(self, tur_list):
        self.tur_list = tur_list

    def get_open_list(self):
        return self.open_list

    def set_open_list(self, open_list):
        self.open_list = open_list

    def get_highest_list(self):
        return self.highest_list

    def set_highest_list(self, highest_list):
        self.highest_list = highest_list

    def __init__(self, code, price_list, wmacd_list, diff_list, dea_list, tur_list, highest_list, open_list):
        self.code = code
        self.price_list = price_list
        self.wmacd_list = wmacd_list
        self.diff_list = diff_list
        self.dea_list = dea_list
        self.tur_list = tur_list
        self.highest_list = highest_list
        self.open_list = open_list
