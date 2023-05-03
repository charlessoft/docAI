# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""

from flask_apscheduler import APScheduler

# from flask_docs import ApiDoc

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

# def job():
#     print(
#         'job thread_id-{0}, process_id-{1}'.format(threading.get_ident(), os.getpid()))
#     time.sleep(50)
# jobstores = {
#                'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
#      }
# executors = {
#     'default': ProcessPoolExecutor(20),
#     # 'processpool': ProcessPoolExecutor(10)
# }
# job_defaults = {
#     'coalesce': False,
#     'max_instances': 20
# }
# sched = BackgroundScheduler(
#     timezone='MST', job_defaults=job_defaults, executors=executors,jobstores=jobstores)
# sched.add_job(job, 'interval', id='3_second_job', seconds=3)
# sched.start()

# BackgroundScheduler

dics = {"trigger": "cron", "second": "*/5"}

# class APSchedulerEx(APScheduler):
#     def __init__(self, scheduler=None, app=None):
#         super(APSchedulerEx,self).__init__(scheduler,app)
#
#     def get_job_result(self):
#         pass

scheduler = APScheduler()
# scheduler.add_job(func=job, id='4_second_job', **dics)
# apidoc = ApiDoc()
