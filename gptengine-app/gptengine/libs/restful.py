# -*- coding: utf-8 -*-
# coding:utf-8
from flask import jsonify, abort

# 定义状态码
from gptengine.libs.error_code import ParameterException, NotFound, ServerError, Success


class HttpCode(object):
    ok = 200
    paramserror = 400
    unautherror = 401
    servererror = 500
    nofounderror = 404


def restful_result(code, message, data):
    return jsonify({
        "code": code,
        "message": message,
        "data": data,
    })


def success(message="", data=None):
    suc = Success(msg=message, data=data)
    return restful_result(suc.code, suc.msg, suc.data)
    # return Success(msg=message,data=data)
    # return restful_result(code=HttpCode.ok, message='successful!' if message is "" else message, data=data)


def unauth_error(message=""):
    return restful_result(code=HttpCode.unautherror, message=message, data=None)


def params_error(message=""):
    paramerr = ParameterException()
    return restful_result(code=paramerr.code, message=message, data=None)


def server_error(message=""):
    return ServerError()
    # return restful_result(code=HttpCode.servererror, message=message or '服务器内部错误', data=None)


def notfound_error(message=""):
    # return NotFound()
    notfound = NotFound()
    return restful_result(code=notfound.code, message=message, data=None)


def custom_abord(http_status_code, *args, **kwargs):
    # 只要http_status_code 为400， 报参数错误
    if http_status_code == 400:
        # abort(make_result(code=Code.NO_PARAM))
        return params_error("ddafaf")
    # 正常返回消息
    return abort(http_status_code)
