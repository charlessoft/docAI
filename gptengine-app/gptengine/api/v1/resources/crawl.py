# -*- coding: utf-8 -*-
from flask_restful import Resource, Api
from sqlalchemy.sql import func

from gptengine.api.v1 import api
from gptengine.common.models.accounts import Accounts, account_schema
from gptengine.libs import restful

api_wrap = Api(api)


@api_wrap.resource('/crawl')  # Create a URL route to this resource
class CrawlResource(Resource):  # Create a RESTful resource
    def __init__(self):
        pass
    def post(self):  # Create GET endpoint
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
        account = Accounts.query.filter_by(biz=biz).first()
        if account:
            return restful.success(data=account_schema.dump(account))
        return restful.success("xxx")


@api_wrap.resource('/getaccounts')  # Create a URL route to this resource
class GetAccountsResource(Resource):  # Create a RESTful resource
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
        # c=Accounts.query.all()
        # print(c)
        account = Accounts.query.order_by(Accounts.collect).first()
        if account:
            account.collect = func.now()
            account.save()
            return restful.success(data=account_schema.dump(account))

