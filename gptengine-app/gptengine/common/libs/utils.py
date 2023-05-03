# -*- coding: utf-8 -*-
import functools

import requests
from flask import request, current_app, jsonify, g
from itsdangerous import Serializer
from sqlalchemy.util import OrderedDict

from gptengine import constants
from gptengine.common.models.auth_admin import AuthAdmin
from gptengine.extensions import redis_store
from gptengine.libs import restful
import base64
import hashlib
import hmac
import json
import re
import time
import uuid
from urllib.parse import quote_plus

def notify_dingding(url, content):
    """
    钉钉消息通知
    :param url:
    :param content:
    :return:
    """
    pass





def get_obj_attr(obj, field):
    """
    :param obj:
    :param field:
    :return:
    """
    for key in field.split("."):
        obj = getattr(obj, key)
        if obj is None:
            break
    return obj


def get_obj_key_fmt(keys):
    """
    :param keys:
    :return:
    'asset.asset_category.name' -> 'asset_asset_category_name' -> 'asset_category_name'
    """
    return "_".join(list(OrderedDict.fromkeys("_".join(keys.split(".")).split("_"))))


def unpack_obj(obj, *args, recurse=False):
    """
    把obj 对象变成字典
    :param obj:
    :param args:
    :param recurse:
    :return:
    """
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        fields = args[0]
    else:
        fields = args
    if not recurse:
        return {field: getattr(obj, field) for field in fields}
    else:
        return {get_obj_key_fmt(field): get_obj_attr(obj, field) for field in fields}


def unpack_objs(objs, *args, recurse=False):
    """
    for循环unpack_obj变成字典
    :param objs:
    :param args:
    :param recurse:
    :return:
    """
    res = []
    for item in objs:
        ret = unpack_obj(item, *args, recurse=recurse)
        res.append(ret)
    return res



def login_required(view_func):
    @functools.wraps(view_func)
    def verify_token(*args, **kwargs):
        try:
            # 在请求头上拿到token
            token = request.headers["X-Token"]
        except Exception:
            # 没接收的到token,给前端抛出错误
            # 这里的code推荐写一个文件统一管理。这里为了看着直观就先写死了。
            # return jsonify(code=4103, msg='缺少参数token')
            return restful.params_error('未登录')

        # s = Serializer(constants.SECRET_KEY)
        # s = Serializer(constants.SECRET_KEY)
        p = redis_store.pipeline()
        users = p.get("user_token_%s" % (token)).execute()
        if users:
            if len(users)>0:
                user = users[0]
        if not user:
            return jsonify(code=50008, msg="登录已过期")
        # g.user = user
        g.user = AuthAdmin.query.filter_by(username=str(user, encoding="utf-8")).first()
        # menus = unpack_objs(user.permissions, 'id', 'pid', 'name', 'title')
        print(g.user.permission_details)


        # try:
        #     s.loads(token)
        # except Exception as e:
        #     current_app.logger.error(e)
        #     return jsonify(code=4101, msg="登录已过期")
        return view_func(*args, **kwargs)
    return verify_token


def notify_dding(content):
    try:
        accesstoken_url = 'https://oapi.dingtalk.com/robot/send?access_token=4e27925ce9df0372171763c071b36bb442cdbf296f315484b9cb165f331da225'
        secret = 'SEC618a0dffd91ebf7db4c9c00e2a82b863bc6181858cadbdbf1655ca6dcd2fd1cc'
        timestamp = int(round(time.time() * 1000))
        secret_enc = secret.encode()
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode()
        print(string_to_sign_enc)
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = quote_plus(base64.b64encode(hmac_code))

        url = '%s&timestamp=%s&sign=%s' % (accesstoken_url, timestamp, sign)
        data = {"msgtype": "text", "text": {"content": content}}
        headers = {'Content-Type': 'application/json;charset=UTF-8'}

        r = requests.post(url, data=json.dumps(data), headers=headers, verify=False, timeout=20)
        print(r.content)
    except Exception as e:
        print(e)
