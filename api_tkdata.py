#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '数据接口'
__author__ = 'JN Zhang'
__mtime__ = '2018/3/9'
"""
import json

from flup.server.fcgi import WSGIServer

from config import mod_config
from t_redis.redis_manager import RedisManager


def fun_tk_data(str_query):
    result_json = {"code": "200", "data": ""}
    if str_query == "" or "code=" not in str_query:
        return {"code": "500", "data": ""}
    else:
        list_query = str_query.split("=")
        for i in range(len(list_query)):
            if list_query[i] == "code":
                rm = RedisManager()
                result = rm.get_data(str(list_query[i + 1]))
                result_json["data"] = str(result).replace("u'", "'")
                result_json["tk_code"] = str(list_query[i + 1])
                return result_json
    return result_json


def fun_wm_data(str_query):
    result_json = {"code": "200", "data": ""}
    if str_query == "" or "date=" not in str_query:
        return {"code": "500", "data": ""}
    else:
        list_query = str_query.split("=")
        for i in range(len(list_query)):
            if list_query[i] == "date":
                rm = RedisManager()
                result = rm.get_data("wm_" + str(list_query[i + 1]))
                result_json["date"] = str(list_query[i + 1])
                result_json["data"] = str(result).replace("u'", "'")
                return result_json
    return result_json


def fun_version():
    result_json = {"code": "200", "data": ""}
    rm = RedisManager()
    result = rm.get_data("tk_version")
    result_json["data"] = str(result)
    return result_json


def myapp(environ, start_response):
    str_query = str(environ["QUERY_STRING"])
    script_filename = str(environ["SCRIPT_FILENAME"])
    if script_filename.split("/")[-1] == "tkdata":
        __result = fun_tk_data(str_query)
        start_response("200 OK", [('Content-Type', 'text/plain')])
        return [json.dumps(__result)]
    elif script_filename.split("/")[-1] == "wmdata":
        __result = fun_wm_data(str_query)
        start_response("200 OK", [('Content-Type', 'text/plain')])
        return [json.dumps(__result)]
    elif script_filename.split("/")[-1] == "tk_version":
        __result = fun_version()
        start_response("200 OK", [('Content-Type', 'text/plain')])
        return [json.dumps(__result)]
    else:
        start_response('404 ERROR', [('Content-Type', 'text/plain')])
        return [json.dumps({"code": "404", "data": ""})]


def start_api_tkdata():
    WSGIServer(myapp, bindAddress=(mod_config.get_config("server", "server_host"), int(mod_config.get_config("server", "tk_data_port")))).run()


if __name__ == "__main__":
    start_api_tkdata()
