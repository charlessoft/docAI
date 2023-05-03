# -*- coding: utf-8 -*-
import codecs
import json
import time

from flask import request
from flask_restful import Resource, Api
from flask_restplus import reqparse

from mobile.api.v1 import api
from mobile.extensions import redis_client
from mobile.libs import restful

api_wrap = Api(api)


class MapResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('key', type=str, location=['json', 'args'], required=True, help="no key")

    def get(self):
        req = self.parser.parse_args()
        key = req['key']
        bret = redis_client.exists(key)
        if bret:
            return restful.success(data=eval(redis_client.get(key)))
        else:
            return restful.success("不存在:%s" %(key))

    def delete(self):
        req = self.parser.parse_args()
        key = req['key']
        ret = redis_client.exists(key)
        if ret:
            redis_client.delete(key)
            return restful.success("删除成功:%s" %(key))
        return restful.success("不存在mobile:%s" %(key))

    def post(self):
        pass

class MapQueueResource(Resource):
    def __init__(self):
        self.keylist = 'keylist'
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('key', type=str, location=['json', 'args'], required=True, help="no key")
        self.post_parser.add_argument('value', type=str, location=['json', 'args'], required=False, help="no value")

        self.get_parser.add_argument('bloop', type=bool, location=['json', 'args'], request=False, default=True,
                                 help='no bloop')
        self.get_parser.add_argument('key', type=str, location=['json', 'args'], required=True, help="no key")

    def get(self):
        # mobile = redis_client.rpoplpush('mobilelist', 'mobilelist')
        req = self.get_parser.parse_args()
        key = redis_client.rpop(self.keylist)
        # mobile['updatetime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        bret = redis_client.exists(key)
        if not bret:
            # 如果不存在,返回空
            redis_client.lpop(self.keylist)
            return restful.success(data={})
        else:
            value=eval(redis_client.get(key))
            value['updatetime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            redis_client.set(key,json.dumps(value))
            if req['bloop']:
                redis_client.lpush(self.keylist,key)
        return restful.success(data=value)

    def post(self):
        req = self.post_parser.parse_args()
        key = req['key']
        ret = redis_client.exists(key)
        if not ret:
            redis_client.set(key, json.dumps(request.get_json(force=True)))
            redis_client.lpush(self.keylist, key)
            return restful.success("上传成功")
        else:
            return restful.success("已经存在:%s" % (key))

