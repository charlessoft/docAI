# -*- coding: utf-8 -*-
from flask import request, jsonify
from flask_restful import Resource, Api
from sqlalchemy.sql import func

from gptengine.api.v1 import api
from gptengine.common.models.accounts import Accounts, account_schema
from gptengine.common.models.menu import Menu
from gptengine.common.models.role_menu import Role_Menu
from gptengine.common.models.user_role import User_Role
from gptengine.libs import restful

api_wrap = Api(api)


@api.route('/find_all_menu')
def find_all_menu():
    '''
    根据用户id获取菜单
    :return:
    '''
    res_dir = request.get_json()
    # user_id = res_dir.get("uuid")
    user_id = None
    data = constructMenuTrees(user_id=user_id)  # 获取菜单树
    return jsonify(code=200, msg="ok", data=data)


def constructMenuTrees(parentId=0, user_id=None):
    '''
    通过递归实现根据父ID查找子菜单,如果传入用户id则只查询该用户的权限否则查询所有权限,一级菜单父id默认是0
    1.根据父ID获取该菜单下的子菜单或权限
    2.遍历子菜单或权限，继续向下获取，直到最小级菜单或权限
    3.如果没有遍历到，返回空的数组，有返回权限列表
    :param user_id:
    :param parentId:
    :return:dict
    '''
    if user_id:
        menu_data = Menu.query.join(Role_Menu, Menu.id == Role_Menu.menu_id).join(User_Role,
                                                                                  User_Role.role_id == Role_Menu.role_id).filter(
            User_Role.user_id == user_id).filter(Menu.parent_id == parentId).order_by('order_num').all()
    else:
        menu_data = Menu.query.filter(Menu.parent_id == parentId).order_by('order_num').all()
    menu_dict = menu_to_dict(menu_data)
    if len(menu_dict) > 0:
        data = []
        for menu in menu_dict:
            menu['children_list'] = constructMenuTrees(menu['id'], user_id)
            data.append(menu)
        return data
    return []


def menu_to_dict(result):
    '''
    格式化菜单字段显示顺序
    :param result:
    :return:
    '''
    data = []
    for menu in result:
        child = {
            "id": menu.id,
            "menu_name": menu.menu_name,
            "parent_id": menu.parent_id,
            "order_num": menu.order_num,
            "url": menu.url,
            "menu_type": menu.menu_type,
            "visible": menu.visible,
            "perms": menu.perms,
            "icon": menu.icon,
            "is_frame": menu.is_frame,
            "create_by": menu.create_by,
            "created_at": menu.created_at,
            "update_by": menu.update_by,
            "updated_at": menu.updated_at,
            "remark": menu.remark,
            "route_name": menu.route_name,
            "route_path": menu.route_path,
            "route_cache": menu.route_cache,
            "route_component": menu.route_component,
        }
        data.append(child)
    return data
