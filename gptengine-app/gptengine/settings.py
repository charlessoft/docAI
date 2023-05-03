# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
import os

from environs import Env

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL", default="xx")
SECRET_KEY = env.str("SECRET_KEY", default="xx")
BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False
CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
SQLALCHEMY_TRACK_MODIFICATIONS = False
WEBPACK_MANIFEST_PATH = "webpack/manifest.json"
SCHEDULER_API_ENABLED = True  # scheduler api


# JOB_STORE = "sqlite:////tmp/jobs.sqlite"
DEBUG = False
if DEBUG:
    # TEXTMINER_ROOT_FOLDER = "/tmp/tm-gptengine/"
    TEXTMINER_ROOT_FOLDER = env.str(
        "TEXTMINER_ROOT_FOLDER",
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    )
else:
    TEXTMINER_ROOT_FOLDER = env.str(
        "TEXTMINER_ROOT_FOLDER",
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    )
    print("====")
    # print(env.str('TEXTMINER_ROOT_FOLDER', os.path.dirname(os.path.realpath(__file__))))
    print(TEXTMINER_ROOT_FOLDER)
    print("=====")
# print(os.path.dirname(os.path.realpath(__file__)))
# sys.exit(1)
RESTFUL_API_DOC_EXCLUDE = []
CACHE_FOLDER = os.path.join(TEXTMINER_ROOT_FOLDER, "cache")

# job
JOB_URL = env.str("JOB_URL", default="http://gptengine.job.url:8889/scheduler")
JOB_STORE = "sqlite:///%s/jobs.sqlite" % (CACHE_FOLDER)
print(JOB_STORE)

FLASK_PORT = 18883
# API_DOC_MEMBER = ['api_1_0_blueprint','api']
# os.putenv('TEXTMINER_ROOT_FOLDER','%s'% os.getcwd())
# os.environ['TEXTMINER_ROOT_FOLDER']='%s'% os.getcwd()
# print(os.environ.get('TEXTMINER_ROOT_FOLDER'))

# ROOT_FOLDER = env.str('ROOT_FOLDER', os.path.dirname(os.path.realpath(__file__)))
# OUTPUT_FOLDER=os.path.join(ROOT_FOLDER,'output')


swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "swagger",
            "route": "/swagger.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/api/docs",
}
