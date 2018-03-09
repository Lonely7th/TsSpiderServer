#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '日志管理类'
__author__ = 'JN Zhang'
__mtime__ = '2018/2/28'
"""
import os
from datetime import datetime


def add_error_logs(tag, code, content):
    path = os.path.dirname(os.path.abspath(__file__)) + "/logs_error.txt"
    fo = open(path, "a")
    log_dict = {
        "tag": tag,
        "code": code,
        "content": content,
        "created_time": str(datetime.now().date())+" "+str(datetime.now().time())
    }
    fo.write(str(log_dict)+"\n")
    fo.close()


def add_info_logs(tag, content):
    path = os.path.dirname(os.path.abspath(__file__)) + "/logs_info.txt"
    fo = open(path, "a")
    log_dict = {
        "tag": tag,
        "content": content,
        "created_time": str(datetime.now().date())+" "+str(datetime.now().time())
    }
    fo.write(str(log_dict) + "\n")
    fo.close()
