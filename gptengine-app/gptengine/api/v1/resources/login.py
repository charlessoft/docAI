# -*- coding: utf-8 -*-


import requests
from flask import current_app as app, request, session, current_app
from flask.json import jsonify
from flask_cors import CORS
# from pyquery import PyQuery as pq
from gptengine import constants
from gptengine.api.v1 import api
from gptengine.api.v1.resources.auth import generate_tree
from gptengine.common.libs.utils import unpack_objs, notify_dding
from gptengine.common.models.auth_admin import AuthAdmin, AuthPermissionRule
from gptengine.common.models.menu import Menu
from gptengine.common.models.role import Role
from gptengine.common.models.user import User
from gptengine.common.models.user_role import User_Role
from gptengine.extensions import redis_store
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from gptengine.libs import restful

CORS(api)


def create_token(user_id, user_name, role_list):
    '''
    生成token
    :param api_user:用户id
    :return: token
    '''
    # 第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    # 第二个参数是有效期(秒)
    s = Serializer(constants.SECRET_KEY, expires_in=constants.TOKEN_REDIS_EXPIRES)
    # 接收用户id转换与编码
    token = None
    try:
        token = s.dumps({"id": user_id, "name": user_name, "role": role_list}).decode("ascii")
        print(token)
    except Exception as e:
        app.logger.error("获取token失败:{}".format(e))
    return token


def verify_token(token):
    '''
    校验token
    :param token:
    :return: 用户信息 or None
    '''
    # 参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer(constants.SECRET_KEY)
    try:
        # 转换为字典
        data = s.loads(token)
        return data
    except Exception as e:
        app.logger.error(f"token转换失败:{e}")
        return None


def login_required(*role):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            try:
                # 在请求头上拿到token
                token = request.headers["Authorization"]
            except Exception as e:
                # 没接收的到token,给前端抛出错误
                return jsonify(code=400, msg='缺少参数token')
            s = Serializer(constants.SECRET_KEY)
            try:
                user = s.loads(token)
                if role:
                    # 获取token中的权限列表如果在参数列表中则表示有权限，否则就表示没有权限
                    user_role = user['role']
                    result = [x for x in user_role if x in list(role)]
                    if not result:
                        return jsonify(code=400, msg="权限不够")
            except Exception as e:
                return jsonify(code=400, msg="登录已过期")
            return func(*args, **kw)

        return wrapper

    return decorator




@api.route('/login', methods=["POST"])
def login():
    """
        ping->pong
        ---
        tags:
          - health
        produces:
         - application/json
        responses:
          200:
            description: successful operation
            example: "running ok!"
     """
    dic = request.json

    # 获取前端传过来的参数
    username = dic.get("username")
    password = dic.get("password")
    captcha = dic.get('captcha')
    ticket = dic.get('ticket')

    # 判断错误次数是否超过限制,如果超过限制则返回

    cache_captcha = redis_store.get("image_code_%s" % (ticket))
    # p = redis_store.pipeline()
    # cache_captcha = p.get("image_code_%s" % (ticket)).execute()
    if str(cache_captcha, encoding='utf-8').lower() != captcha.lower():
        return restful.params_error('验证码不正确')

    # 校验参数
    if not all([username, password]):
        return restful.params_error('用户名或密码不能为空')

    user_ip = request.remote_addr  # 用户的ip地址
    try:
        access_nums = redis_store.get('access_nums_%s' % (user_ip))
    except Exception as e:
        current_app.logger.error(e)
    else:
        if access_nums is not None and int(access_nums) > constants.LOGIN_ERROR_MAX_TIMES:
            errmsg = 'ip: %s ,username: %s ,错误次数过多,请稍后重试' %(user_ip, username)
            notify_dding(errmsg)
            return restful.params_error(errmsg)

    # try:
    #     user = User.query.filter_by(user_name=username).first()
    # except Exception as e:
    #     app.logger.error("login error：{}".format(e))
    #     return jsonify(code=400, msg="获取信息失败")
    # if user is None or not user.check_password(password) or user.del_flag == 2 or user.status == 2:
    #     return jsonify(code=400, msg="用户名或密码错误")

    try:
        admin = AuthAdmin.query.filter_by(username=username, password=password).first()
    except Exception as e:
        app.logger.error("login error：{}".format(e))
        return restful.params_error('用户名或密码错误')
    # if user is None or not user.check_password(password) or user.del_flag == 2 or user.status == 2:
    #     return jsonify(code=400,msg='用户名密码错误')

    # 获取用户信息，传入生成token的方法，并接收返回的token
    # 获取用户角色
    # user_role = Role.query.join(User_Role, Role.id == User_Role.role_id).join(User,
    #                                                                           User_Role.user_id == user.id).filter(
    #     User.id == user.id).all()
    # role_list = [i.role_key for i in user_role]
    # admin = AuthAdmin.query.filter_by(username=username,password=password).first()
    # if admin:
    #     admin.roles
    # [x for x in user_role if x in list(role)]
    if not admin:
        try:
            redis_store.incr('access_nums_%s' % (user_ip))
            redis_store.expire('access_nums_%s' % (user_ip), constants.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            current_app.logger.error(e)
        return restful.params_error('用户名或密码错误')
    # 验证成功了.

    token = create_token(admin.id, admin.username, '123')
    data = {'token': token, 'userId': 'admin.id', 'userName': admin.username, 'nickname': 'user.nickname'}
    # 记录登录ip将token存入rerdis
    try:
        p = redis_store.pipeline()
        p.setex("user_token_%s" % (token), constants.TOKEN_REDIS_EXPIRES, dic["username"]).execute()

    except Exception as e:
        return jsonify(code=400, msg="登录失败")
    if token:
        # 把token返回给前端
        # return jsonify(code=200, msg="登录成功", data=data)
        return jsonify({"code": 200, "data": {"token": token}})
    else:
        return jsonify(code=400, msg="请求失败", data=token)

    # users = casbinmgr.get_all_subjects()
    # if dic["username"] in users:
    #     if dic["username"] == "admin" and dic["password"] == "fzmd2021enter":
    #         p = redis_store.pipeline()
    #         token = create_token()
    #         p.setex("user_token_%s" % (token), constants.TOKEN_REDIS_EXPIRES, dic["username"]).execute()
    #         return jsonify({"code": 200, "data": {"token": token}})
    #     elif dic["username"] == "alice" and dic["fzmd2021enter"] == "alice":
    #         return jsonify({"code": 200, "data": {"token": "alice-token"}})
    #     else:
    #         return jsonify({"code":400,"msg":"login fail"})
    # return jsonify({"code":400,"msg":"login fail"})
    # return restful.success(data={"Token": "xxx"})


@api.route('/info', methods=["GET"])
def info():
    """
        ping->pong
        ---
        tags:
          - health
        produces:
         - application/json
        responses:
          200:
            description: successful operation
            example: "running ok!"
     """
    X_Token = request.headers.get("X-Token", '')
    p = redis_store.pipeline()
    users = p.get("user_token_%s" % (X_Token)).execute()
    user = None
    # for test
    if len(users) > 0:
        user = users[0]
    # user = 'admin'
    # for test
    if not user:
        return restful.notfound_error('not found')
    user = AuthAdmin.query.filter_by(username=str(user, encoding="utf-8")).first()
    menus = unpack_objs(user.permissions, 'id', 'pid', 'name', 'title')

    # menus = []
    # for role in user.roles:
    #     ls = [item.id for item in role.permission_rules]
    #     # AuthPermissionRule.query.filter_b()
    #     tmps = AuthPermissionRule.query.filter(AuthPermissionRule.id.in_(ls)).all()
    #     menus.extend(unpack_objs(tmps, 'id', 'pid', 'name', 'title'))

    # shoes = Shoe.query.filter(Shoe.id.in_(my_list_of_ids)).all()

    menus = generate_tree(menus, 0)
    print(menus)
    outout = []

    def parse_component(pid, title):
        if title.find('Layout') >= 0:
            return 'Layout'
        else:
            return title + '/index'

    for menu in menus:
        dic = {
            'component': parse_component(menu['pid'], menu['name']),
            'path': '/' + menu['name'],
            'meta': {
                'title': menu['title'],
                'icon': 'form'
            },
            'children': menu['children']
        }

        for child in dic['children']:
            child['component'] = parse_component(child['pid'], child['name'])
            child['path'] = '/' + child['name']
            child['meta'] = {
                'title': child['title'],
                'icon': 'form'
            }
        outout.append(dic)

    print("++++++++++++++++")

    data = {"roles": [role.name for role in user.roles],
            "introduction": "I am a super administrator",
            "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
            "name": user.username,
            "menus":
                outout

            }
    print(data)
    # return jsonify({"code": 200, "data": {"roles": ["admin"],
    #                                       "introduction": "I am a super administrator",
    #                                       "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
    #                                       "name": "Super Admin",
    #                                       "menus":
    #                                           [{
    #                                               "path": "/system",
    #                                               "redirect": "/menu",
    #                                               "component": "Layout",
    #                                               "meta": {
    #                                                   "title": "系统管理",
    #                                                   "icon": "form"
    #                                               },
    #                                               "children": [{
    #                                                   "path": "/menu",
    #                                                   "name": "menu",
    #                                                   "component": "menu/index",
    #                                                   "meta": {
    #                                                       "title": "菜单管理",
    #                                                       "icon": "table"
    #                                                   }
    #                                               }]
    #                                           }]
    #
    #                                       }})

    return jsonify({"code": 200, "data": data})
    # return restful.success(data={"role": "admin"})


@api.route('/user/logout', methods=["POST"])
def logout():
    return jsonify({
        'code': 200,
        'data': 'success'
    })
