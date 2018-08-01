#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JN Zhang'
__mtime__ = '2018/6/25'
"""
import datetime

from core.c_strategy.strategy_3 import TsStrategy3
from core.wmacd_utils import WmacdUtils

if __name__ == "__main__":
    # 恢复20180525的数据
    wu = WmacdUtils()
    wu.update_w_macd("2018-07-21")
    # 重新计算strategy_3
    st3 = TsStrategy3()
    st3.update_redis("2018-07-21")
