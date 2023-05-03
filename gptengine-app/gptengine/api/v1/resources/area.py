# -*- coding: utf-8 -*-


from flask_restful import Resource, Api

from gptengine.api.v1 import api
from gptengine.common.libs import utils
from gptengine.common.models.accounts import Accounts, account_schema
# from gptengine.common.models.area_code_2020 import AreaCode2020
from gptengine.common.models.area_code_2020 import AreaCode2020, area_schema
from gptengine.libs import restful

api_wrap = Api(api)
g_map={}

# @api_wrap.resource('/provinces/<name>')  # Create a URL route to this resource
# class ProvinceResource(Resource):  # Create a RESTful resource
#     def get(self, name):  # Create GET endpoint
#         """
#         ping->pong
#         ---
#         tags:
#           - health
#         produces:
#          - application/json
#         responses:
#           200:
#             description: successful operation
#             example: "running ok!"
#         """
#         account = AreaCode2020.query.filter_by(name=name)
#         if account:
#             return restful.success(data=account_schema.dump(account))
#         return restful.success("xxx")
# resdic = {}


def enumarea(code, level, dic, retdic):
    title = ''
    if level == 1:
        title = 'city'
    elif level == 2:
        title = 'district'
    elif level == 3:
        title = 'street'
    elif level == 4:
        title = 'community'
    else:
        return
    # elif level == 5:
    #     title = 'community'
    retdic.setdefault(title, [])
    if level > 4:
        return
    res = AreaCode2020.query.filter_by(pcode=code).all()
    for item in res:
        tmpdic = area_schema.dump(item)
        retdic[title].append(tmpdic)
        enumarea(item.code, level + 1, {}, tmpdic)


@api_wrap.resource('/provinces/<code>')  # Create a URL route to this resource
class ProvinceResource(Resource):  # Create a RESTful resource
    def get(self, code):  # Create GET endpoint
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
        # provinces = AreaCode2020.query.all()
        lst = []
        cityarr = []
        retdic = {}
        enumarea(code, 1, {}, retdic)
        print(retdic)
        return restful.success(data=retdic)
        # citys = AreaCode2020.query.filter_by(pcode=code).all()
        # if citys:
        #     for city in citys:
        #         districts = AreaCode2020.query.filter_by(pcode=city.code).all()
        #         for district in districts:
        #             streets = AreaCode2020.query.filter_by(pcode=district.code).all()
        #             for street in streets:
        #                 communitys = AreaCode2020.query.filter_by(pcode=street.code).all()
        #
        #     return restful.success(data=area_schema.dump(citys, many=True))

        # provinces = AreaCode2020.query.filter_by(name='北京市').first()
        # if provinces:
        #     return restful.success(data=area_schema.dump(provinces,many=True))
        # return restful.success("xxx")


def get(code):
    communitys = AreaCode2020.query.filter_by(level=5, pcode=code).all()
    # provinces = AreaCode2020.query.filter_by(name='北京市').first()
    if communitys:
        return restful.success(data=area_schema.dump(communitys, many=True))
    return restful.success("xxx")


@api_wrap.resource('/communitys/<code>')
class CommumitysResource(Resource):
    def get(self, code):
        if code in g_map:
            return restful.success(data=g_map[code])
        communitys = AreaCode2020.query.filter_by(level=5, pcode=code).all()
        # provinces = AreaCode2020.query.filter_by(name='北京市').first()
        if communitys:
            g_map[code]=area_schema.dump(communitys, many=True)
            return restful.success(data=g_map[code])
        return restful.success("xxx")


@api_wrap.resource('/streets/<code>')
class StreetsResource(Resource):
    def get(self, code):
        if code in g_map:
            return restful.success(data=g_map[code])
        communitys = AreaCode2020.query.filter_by(level=4, pcode=code).all()
        if communitys:
        # provinces = AreaCode2020.query.filter_by(name='北京市').first()
            g_map[code]=area_schema.dump(communitys, many=True)
            return restful.success(data=g_map[code])
        return restful.success("xxx")


@api_wrap.resource('/districts/<code>')
class DistrictsResource(Resource):
    def get(self, code):
        if code in g_map:
            return restful.success(data=g_map[code])
        streets = AreaCode2020.query.filter_by(level=3, pcode=code).all()
        # provinces = AreaCode2020.query.filter_by(name='北京市').first()
        if streets:
            g_map[code]=area_schema.dump(streets, many=True)
            return restful.success(data=g_map[code])
        return restful.success("xxx")


@api_wrap.resource('/citys/<code>')
class CitysResource(Resource):
    def get(self, code):
        if code in g_map:
            return restful.success(data=g_map[code])
        districts = AreaCode2020.query.filter_by(level=2, pcode=code).all()
        # provinces = AreaCode2020.query.filter_by(name='北京市').first()
        if districts:
            g_map[code]=area_schema.dump(districts, many=True)
            return restful.success(data=g_map[code])
        return restful.success("xxx")


@api_wrap.resource('/Fujian')  # Create a URL route to this resource
class FujianResource(Resource):  # Create a RESTful resource
    def get(self):
        # retdic = {}
        # enumarea("福建", 3, {}, retdic)
        # print(retdic)
        code = {
            "code": 350000000000,
            "level": 1,
            "name": "福建省",
            "pcode": 0
        }
        districts = AreaCode2020.query.filter_by(level=2, pcode=code).all()
        if districts:
            return restful.success(data=area_schema.dump(districts, many=True))
        return restful.success("xxx")


@api_wrap.resource('/provinces')  # Create a URL route to this resource
class ProvinceAllResource(Resource):  # Create a RESTful resource
    def get(self):  # Create GET endpoint
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
        # provinces = AreaCode2020.query.all()
        provinces = AreaCode2020.query.filter_by(level=1).all()
        # provinces = AreaCode2020.query.filter_by(name='北京市').first()
        if provinces:
            return restful.success(data=area_schema.dump(provinces, many=True))
        return restful.success("xxx")
