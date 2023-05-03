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

ROOT_FOLDER = env.str(
    "ROOT_FOLDER", os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
)
CACHE_FOLDER = os.path.join(ROOT_FOLDER, "cache")


JOB_STORE = "sqlite:///%s/jobs.sqlite" % (CACHE_FOLDER)
print("====")
# print(env.str('TEXTMINER_ROOT_FOLDER', os.path.dirname(os.path.realpath(__file__))))
print(ROOT_FOLDER)
print(JOB_STORE)
print("=====")

# ROOT_FOLDER = env.str('ROOT_FOLDER', os.path.dirname(os.path.realpath(__file__)))
# OUTPUT_FOLDER=os.path.join(ROOT_FOLDER,'output')
