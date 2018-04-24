#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '文件操作'
__author__ = 'JN Zhang'
__mtime__ = '2018/4/3'
"""
import json
import os
base_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + "/t_bp/bp_result/"


class FileUtils:
    def __init__(self, file_name, _type):
        self.file = open(base_path + file_name, _type)

    def insert_line(self, line):
        if self.file:
            self.file.write(line + "\n")

    def raed_line(self):
        while True:
            line = self.file.readline()
            if '' == line:
                break
            yield line


if __name__ == "__main__":
    f_utils = FileUtils("test.txt", "a+")
    f_utils.insert_line("date:2018-04-24")
    f_utils.insert_line("buy:" + json.dumps(["000001", 7.89, 200]))
    # for i in f_utils.raed_line():
    #     print(str(i).strip())
