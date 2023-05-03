# # -*- coding: utf-8 -*-
from flask import Blueprint
from flask_cors import CORS

# from flask_restplus import Api, Namespace
# from flask_restful import Api
# from flask_restful_swagger import swagger
# from flask_restplus import Api


api = Blueprint("api_v1", __name__)

# flask_restplus.abort = custom_abord
# restful api
# api_wrap = Api(api)

# 1. flask_restplus 自带swagger 不全,很多需要定义的内容,细节不能满足
# 2. flask-restful-swagger 同上
# 3. flask-swagger 只支持普通的api写法
# 4. flasgger 普通api 和restful api都支持.手写定义yaml更适合.繁琐一些.

CORS(api)
from gptengine.api.v1.resources import *
