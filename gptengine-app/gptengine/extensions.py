# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from celery import Celery
# from flasgger import Swagger
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask_redis import FlaskRedis


from gptengine.libs import restful
migrate = Migrate()
db = SQLAlchemy()
redis_store = FlaskRedis()

# from flask_authz import CasbinEnforcer



class Query(BaseQuery):
    def filter_by(self, **kwargs):
        # if 'status' not in kwargs.keys():
        #     kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)
    def get_or_404(self, ident):
        rv = self.get(ident)
        if rv is None:
            raise restful.notfound_error()
        return rv
    def first_or_404(self):
        rv = self.first()
        if rv is None:
            raise restful.notfound_error()
        return rv
db = SQLAlchemy(query_class=Query)
# from flask_apscheduler import APScheduler

# from flask_bcrypt import Bcrypt
# from flask_caching import Cache
# from flask_debugtoolbar import DebugToolbarExtension
# from flask_login import LoginManager
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
# from flask_webpack import Webpack
# from flask_wtf.csrf import CSRFProtect

# bcrypt = Bcrypt()
# csrf_protect = CSRFProtect()
# login_manager = LoginManager()
# db = SQLAlchemy()
# migrate = Migrate()
# cache = Cache()
# debug_toolbar = DebugToolbarExtension()
# webpack = Webpack()
# scheduler = APScheduler()


# swagger = Swagger()
ma = Marshmallow()
