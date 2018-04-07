#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '交易策略03'
__author__ = 'JN Zhang'
__mtime__ = '2018/4/6'
"""
import numpy as np

from bean.tk_wmacd_bean import tkWMacdBean


class TsStrategy3:
    def __init__(self):
        pass

    def get_result(self, __ticker):
        buy_list = list()
        if isinstance(__ticker, tkWMacdBean) and len(__ticker.get_wmacd_list()) > 30:
            if __ticker.get_wmacd_list()[-1] > 0 >= __ticker.get_wmacd_list()[-2]:
                if 0.1 > __ticker.get_diff_list()[-1] > 0:
                    if np.mean(__ticker.get_tur_list()[-5:-1]) < __ticker.get_tur_list()[-1]:
                        buy_list.append(__ticker.get_code())
        return buy_list
