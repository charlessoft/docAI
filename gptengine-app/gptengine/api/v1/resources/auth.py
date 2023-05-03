# -*- coding: utf-8 -*-
import re

import requests
from flask import current_app as app, request, jsonify, send_from_directory, current_app
from pyquery import PyQuery as pq
from sqlalchemy import text

from gptengine.api.v1 import api
from gptengine.common.libs.utils import unpack_obj, unpack_objs
from gptengine.common.models.accounts import Accounts
from gptengine.common.models.auth_admin import AuthAdmin, auth_admin_schema, auth_role_schema, AuthPermissionRule, \
    auth_permission_rule_schema, AuthRole
# from gptengine.common.models.auth_permission_rule import AuthPermissionRule

from gptengine.common.models.casbin_rule import Casbin_Rule
from gptengine.extensions import db
from gptengine.libs import restful


@api.route('/admin/auth/admin/save', methods=["POST"])
def auth_Admin_save():
    # {'id': '', 'password': 'aaa', 'username': 'aaaa', 'checkPassword': 'aaa', 'status': 1, 'roles': [3, 1]}
    dic = request.json
    try:
        roles = AuthRole.query.filter(AuthRole.id.in_(dic['roles'])).all()
        tmpUser = AuthAdmin(username=dic['username'],
                            password=dic['password'],
                            status=dic['status'])
        # print(tmpUser.roles)
        # for role in dic['roles']:
        #     tmpUser.roles.append()
        tmpUser.roles = roles

        tmpUser.save()
        return restful.success(data=auth_admin_schema.dump(tmpUser))
    except Exception as e:
        current_app.logger.error(e)
        return restful.params_error('add fail')


@api.route('/admin/auth/admin/delete', methods=["POST"])
def auth_Admin_delete():
    dic = request.json
    try:
        AuthAdmin.query.filter_by(id=dic['id']).delete()
        return restful.success('ok')
    except Exception as e:
        current_app.logger.error(e)
        return restful.params_error('del fail')


@api.route('/admin/auth/admin/edit', methods=["POST"])
def auth_Admin_edit():
    dic = request.json
    # tmpUser = AuthAdmin.create(**dic)
    rolesid = dic['roles']
    roles = AuthRole.query.filter(AuthRole.id.in_(rolesid)).all()
    user = AuthAdmin.query.filter_by(id=dic['id']).first()
    if user:
        user.user_name = dic['username']
        user.status = dic['status']
        if dic['password']:
            user.password = dic['password']
        user.login_date = dic['last_login_time']
        user.login_ip = dic['last_login_ip']
        user.roles = roles
        user.save()
        return restful.success("ok")
    return restful.notfound_error('no found')


@api.route('/admin/auth/admin/index')
def auth_Admin():
    status = request.args.get("status")
    age = request.args.get("age")
    role_id = request.args.get('role_id')
    username = request.args.get('username')
    # authRoleAdmins = AuthRole.query.filter_by(id=role_id).all()

    # authAdminList  = AuthAdmin.query().all()
    # allauth = AuthAdmin.query.with_entities(AuthAdmin.id, AuthAdmin.username,
    #                                         AuthAdmin.password,
    #                                         AuthAdmin.status, AuthAdmin.last_login_ip, AuthAdmin.last_login_time, AuthAdmin.roles).all()
    allauth = AuthAdmin.query.all()
    lst = []
    if allauth:
        for auth in allauth:
            dicauth={}
            dicauth['roles'] = [role.id for role in auth.roles]
            dicauth.update(unpack_obj(auth, 'id', 'username','password', 'status', 'last_login_ip', 'last_login_time'))
            lst.append(dicauth)

        return restful.success(data={"data":lst,'total':len(lst)})

        # return restful.success(
        #     data={"data": unpack_objs(allauth, 'id', 'username','password', 'status', 'last_login_ip', 'last_login_time'),
        #           "total": len(allauth)})
    else:
        return restful.notfound_error('no found')


@api.route('/admin/auth/role/delete', methods=["POST"])
def auth_Role_Delte():
    dic = request.json
    try:
        AuthRole.query.filter_by(id=dic['id']).delete()
    except Exception as e:
        current_app.logger.error(e)
        return restful.params_error("del fail")
    return restful.success('ok')


@api.route('/admin/auth/role/edit', methods=["POST"])
def auth_Role_Edit():
    dic = request.json
    try:
        AuthRole.query.filter_by(id=dic['id']).update(
            {'name': dic['name'],
             'listorder': dic['listorder'],
             'remark': dic['remark'],
             'status': dic['status']}
        )
        return restful.success('ok')
    except Exception as e:
        current_app.logger.error(e)
        return restful.params_error('edie fail')


@api.route('/admin/auth/role/save', methods=["POST"])
def auth_Role_save():
    dic = request.json
    try:
        tmpRole = AuthRole(name=dic['name'],
                           pid=0,
                           listorder=dic['listorder'],
                           remark=dic['remark'],
                           status=dic['status'],
                           )

        tmpRole.save()
        return restful.success(data=auth_role_schema.dump(tmpRole))
    except Exception as e:
        current_app.logger.error(e)
        return restful.params_error('add fail')


@api.route('/admin/auth/role/index')
def auth_Role():
    allRole = AuthRole.query.with_entities(AuthRole.id, AuthRole.name, AuthRole.status, AuthRole.remark,
                                           AuthRole.listorder).all()
    if allRole:
        return restful.success(data=unpack_objs(allRole, 'id', 'name', 'status', 'remark', 'listorder'))
    else:
        return restful.notfound_error('no found')


@api.route('/admin/auth/role/auth', methods=["POST"])
def auth_Role_auth():
    dic = request.json
    rule_ids = dic['auth_rules']
    role_id = dic['role_id']

    try:
        permision_rules = AuthPermissionRule.query.filter(AuthPermissionRule.id.in_(rule_ids)).all()

        auth_role = AuthRole.query.filter_by(id=role_id).first()
        if auth_role:
            auth_role.permission_rules = permision_rules
            auth_role.save()
    except Exception as e:
        current_app.logger.error(e)
        return restful.params_error('save role permission fail')
    return restful.success("ok")


@api.route('/admin/auth/role/authList')
def auth_RoleList():
    """
     获取授权列表
    :return:
    """

    id = request.args.get('id')
    # admin = AuthAdmin.query.filter_by(id=id).first()
    role = AuthRole.query.filter_by(id=id).first()
    checked_keys = []
    auth_list = []

    allPermissionRole = AuthPermissionRule.query.order_by(
        AuthPermissionRule.id).all()  # .with_entities(AuthRole.id,AuthRole.name,AuthRole.status,AuthRole.remark).all()
    if allPermissionRole:
        data = unpack_objs(allPermissionRole, 'id', 'pid', 'name', 'title', 'status', 'condition', 'listorder')
        auth_list = generate_tree(data, 0)

    if role:
        if role.permission_rules:
            print(role.permission_rules)
            permission_rules = unpack_objs(role.permission_rules, 'id', 'pid')
            for permission in permission_rules:
                checked_keys.append(permission['id'])
            # check_keys = generate_tree(permissions, 0)
            # checked_keys = [0,1,2,3]
            print(checked_keys)

            return restful.success(data={'auth_list': auth_list, 'checked_keys': checked_keys})
        else:
            return restful.success(data={'auth_list': auth_list})
    return restful.params_error('no found')


def generate_tree(source, parent):
    tree = []
    for item in source:
        if item["pid"] == parent:
            item["children"] = generate_tree(source, item["id"])
            tree.append(item)
    return tree


@api.route('/admin/auth/permission_rule/index')
def auth_Permission_Rule():
    status = request.args.get("status")
    age = request.args.get("age")
    role_id = request.args.get('role_id')
    username = request.args.get('username')
    authRoleAdmins = AuthRole.query.filter_by(id=role_id).all()

    allPermissionRole = AuthPermissionRule.query.order_by(
        AuthPermissionRule.id).all()  # .with_entities(AuthRole.id,AuthRole.name,AuthRole.status,AuthRole.remark).all()
    if allPermissionRole:
        data = unpack_objs(allPermissionRole, 'id', 'pid', 'name', 'title', 'status', 'condition', 'listorder')
        permission_tree = generate_tree(data, 0)
        return restful.success(data=permission_tree)
    else:
        return restful.notfound_error('no found')


@api.route('/admin/auth/permission_rule/delete', methods=["POST"])
def auth_permission_rule_delete():
    dic = request.json
    try:
        # allroles = AuthRole.query.all()
        permission_rule_id = dic['id']
        # 手动删除, todo, 反向查询无法用?
        del_sql = "delete from auth_permission where permission_rule_id=:permission_rule_id"
        db.engine.execute(text(del_sql), {"permission_rule_id": permission_rule_id})
        auth_permision_rule = AuthPermissionRule.query.filter_by(id=permission_rule_id)

        auth_permision_rule.delete()

        # if auth_permision_rule:
        #     print(auth_permision_rule.auth_roles)
        return restful.success('ok')
    except Exception as e:
        return restful.params_error('no found')


@api.route('/admin/auth/permission_rule/save', methods=["POST"])
def auth_permission_rule_save():
    dic = request.json
    try:
        #     condition: ""
        # id: ""
        # listorder: 999
        # name: "test/test1"
        # pid: 26
        # status: 1
        # title: "表11"
        permissionRule = AuthPermissionRule(listorder=dic.get('listorder', 999),
                                            name=dic['name'],
                                            pid=dic['pid'],
                                            status=dic['status'],
                                            title=dic['title']
                                            )
        permissionRule.save()
        return restful.success(data=auth_permission_rule_schema.dump(permissionRule))
    except Exception as e:
        return restful.notfound_error('not found')


@api.route('/admin/auth/admin/roleList')
def auth_role_lst():
    # username=&status=&page=1&limit=20&role_id=
    username = request.args.get('username')
    status = request.args.get('page')
    page = request.args.get('page')
    limit = request.args.get('lilmit')
    role_id = request.args.get('role_id')
    rolelst = AuthRole.query.all()

    if rolelst:
        return restful.success(data=unpack_objs(rolelst, 'id', 'name', 'status', 'remark'))
    else:
        return restful.notfound_error('no found')
    return restful.success()
    # user = User.query.get_or_404(1)
    # return restful.success("gptengine running ok")
