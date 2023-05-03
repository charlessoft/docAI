# -*- coding: utf-8 -*-
import importlib
import os
import sys
from os.path import dirname, abspath, join

import urllib

from celery import Celery


sys.path.append(os.getcwd())
PROJECT_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)

# from gptengine.extensions import swagger
from gptengine.extensions import swagger, db, migrate, ma, redis_store
from gptengine.settings import swagger_config, FLASK_PORT,DEBUG
from gptengine.common.models import testmodel
from gptengine.core.common_util import get_resource_path
from logging.config import fileConfig

# from flask_swagger_ui import get_swaggerui_blueprint
# from jobs.extensions import apidoc
# from gptengine.extensions import scheduler
from flask import Flask, render_template
import logging
# sys.path.append('/Users/charles/workspace/yr_prj/basin/tm/tm-gptengine/demo')
logger = logging.getLogger()

CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERYD_CONCURRENCY = 20
celery = Celery(__name__.split('.')[0], broker=CELERY_BROKER_URL)

def create_app(config_object='gptengine.settings'):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0],
                template_folder=join(PROJECT_DIR, 'gptengine'),
                static_folder=join(PROJECT_DIR, 'gptengine', 'static'))
    app.config.from_object(config_object)
    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    # register_errorhandlers(app)
    # register_shellcontext(app)
    # register_commands(app)

    return app


def init_shell(app):
    @app.cli.command("ishell")
    def shell():
        # lazy import these modules as they are only used in the shell context
        from IPython import embed, InteractiveShell
        import cProfile
        import pdb

        main = importlib.import_module("__main__")

        banner = f"App: poi"
        # from .constants.models import testmodel as models

        ctx = main.__dict__
        ctx.update(
            {
                **testmodel.__dict__,
                "session": db.session,
                "pdb": pdb,
                "cProfile": cProfile,
            }
        )

        with app.app_context():
            ctx.update(app.make_shell_context())
            InteractiveShell.colors = "Neutral"
            embed(user_ns=ctx, banner2=banner)


def register_extensions(app):
    """Register Flask extensions."""

    swagger.config = swagger_config
    swagger.init_app(app)

    # bcrypt.init_app(app)
    # cache.init_app(app)

    #数据库配置
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pa44w0rd@1.15.59.76/MyEducationSys?charset=utf8mb4'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cqtest:%s@106.52.100.60/test?charset=utf8mb4' % (urllib.parse.quote('Pa44w0rd!@#$'))
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['CELERY_BROKER_URL'] = 'redis://1.15.59.76:6379/1'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://1.15.59.76:6379/1'
    app.config['REDIS_URL'] = 'redis://:foo@1.15.59.76:11080/1'
    #debug 输出sql 语句
    #app.config["SQLALCHEMY_ECHO"] = True

    db.init_app(app)
    migrate.init_app(app, db)
    init_shell(app)
    ma.init_app(app)
    redis_store.init_app(app)


    celery.conf.update(app.config)
    # csrf_protect.init_app(app)
    # login_manager.init_app(app)
    # debug_toolbar.init_app(app)
    # migrate.init_app(app, db)
    # webpack.init_app(app)
    # apidoc.init_app(app)

    # scheduler.init_app(app)
    #
    # scheduler.add_listener(my_listener,EVENT_ALL)
    # scheduler.add_listener(my_listener,EVENT_ALL)
    # scheduler.add_listener(my_listener,(EVENT_JOB_ADDED |
    #                                     EVENT_JOB_REMOVED |
    #                                     EVENT_JOB_MODIFIED |
    #                                     EVENT_JOB_EXECUTED |
    #                                     EVENT_JOB_ERROR |
    #                                     EVENT_JOB_MISSED))

    # app, config=swagger_config
    # swagger.init_app(app)
    # swagger.config=swagger_config
    return None


class BadRequest(Exception):
    """将本地错误包装成一个异常实例供抛出"""

    def __init__(self, message, code=400, payload=None):
        self.message = message
        self.code = code
        self.payload = payload

    def to_dict(self):
        return {"code": self.code,
                "message": self.message,
                "data": self.payload}


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error templates."""
        # If a HTTPException, pull the `code` attribute; default to 500
        import traceback

        error_code = getattr(error, 'code', 500)
        logger.error(traceback.format_exc())
        return render_template('{0}.html'.format(error_code)), error_code

    def render_error1(error):
        # return restful.params_error('required invalid! missing file')
        return render_template('{0}.html'.format(500)), 500

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)

    # app.errorhandler(400)(handle_404_error)
    # app.errorhandler(400)(custom_abord)
    # app.register_error_handler(400,BadRequest)

    return None


def register_logging(app):
    abspath = os.path.abspath(os.path.dirname(__file__))
    fileConfig(os.path.join(abspath, './logging_config.ini'))

    # logger = logging.getLogger('thesis_train')
    # app.logger.setLevel(logging.DEBUG)  # 日志模块等级,优先级最大


def register_blueprints(app):
    """Register Flask blueprints."""

    # from gptengine.views.admin import admin
    #
    # app.register_blueprint(admin)

    # from api.v1.resources.index import api
    # app.register_blueprint(api, url_prefix='/api/v1/index')

    from gptengine.api.v1 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1')

    # from gptengine.jobs import jobs as jobs_blueprint
    # app.register_blueprint(jobs_blueprint, url_prefix='/api/v1')

    # app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # from gptengine.api.v1 import api2 as api2_1_0_blueprint
    # app.register_blueprint(api2_1_0_blueprint, url_prefix='/api/v1')

    # from gptengine.user.index import admin
    # app.register_blueprint(admin)

    return None


app = create_app()

# api1 = Api(app)                         #  Create a Flask-RESTPlus API
# #
# @api1.resource('/hello')                   #  Create a URL route to this resource
# class HelloWorld(Resource):            #  Create a RESTful resource
#     def get(self):                     #  Create GET endpoint
#         parser = reqparse.RequestParser(bundle_errors=True)
#         parser.add_argument('model_id', type=str, location=['form', 'json'], required=True, help="缺少model_id")
#         req = parser.parse_args()
#         # return {'hello': 'world'}

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    # Only for debugging while developing
    # scheduler.start()
    app.run(host='0.0.0.0', debug=DEBUG, port=FLASK_PORT)
