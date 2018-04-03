#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '配置管理类'
__author__ = 'JN Zhang'
__mtime__ = '2018/2/26'
"""
import configparser
import os


# 获取config配置文件
def get_config(section, key):
    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/config.conf'
    config.read(path)
    return config.get(section, key)
