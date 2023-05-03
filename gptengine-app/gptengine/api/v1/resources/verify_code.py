# -*- coding: utf-8 -*-
import random
import re
import string

import requests
from flask import current_app as app, request, jsonify, send_from_directory, current_app, make_response, Response
from pyquery import PyQuery as pq
from captcha.image import ImageCaptcha
from werkzeug.wsgi import FileWrapper

from gptengine import constants
from gptengine.api.v1 import api
from gptengine.extensions import redis_store
from gptengine.libs import restful


@api.route('/image_codes')
def get_image_code():
    """
    获取图片验证码
    :param image_code_id: 图片验证码编号
    :return: 验证码图片
    """
    ticket = request.args.get('ticket')
    # ticket = dic.get('ticket')
    # 业务逻辑处理
    # 生成验证码图片
    # 讲验证码真实值与编号保存到redis
    # 返回图片
    # redis_store.set("image_code_%s" %(image_code_id))
    # redis_store.expire("image_code_%s" %(image_code_id),constants.IMAGE_CODE_REDIS_EXPIRES)
    try:
        image = ImageCaptcha()
        text = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        data = image.generate(text)
        w = FileWrapper(data)
        redis_store.setex("image_code_%s" % (ticket), constants.IMAGE_CODE_REDIS_EXPIRES, text)
        # p = redis_store.pipeline()
        #
        # p.setex("image_code_%s" % (image_code_id), constants.IMAGE_CODE_REDIS_EXPIRES, text).execute()
        return Response(w, mimetype="image/jpg", direct_passthrough=True)
        # return restful.success(data={"aa":11})
        # return restful.success()
    except Exception as e:
        current_app.logger.error(e)
        return restful.params_error("image save code fail")
    # resp = make_response(data)
    # resp.headers['Content-Type'] = "image/jpg"
    return "1"

    # user = User.query.get_or_404(1)
    # return restful.success("gptengine running ok")
