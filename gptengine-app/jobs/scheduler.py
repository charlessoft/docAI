import logging
import os
import sys

try:
    sys.path.insert(0, os.getcwd())
except Exception as e:
    print(e)


from logging.config import fileConfig

from apscheduler.events import (
    EVENT_JOB_EXECUTED,
    EVENT_JOB_ERROR,
    EVENT_ALL,
    EVENT_JOB_MISSED,
    EVENT_JOB_ADDED,
    EVENT_JOB_REMOVED,
    EVENT_JOB_MODIFIED,
    EVENT_JOB_MAX_INSTANCES,
    EVENT_EXECUTOR_ADDED,
    EVENT_SCHEDULER_RESUMED,
    EVENT_SCHEDULER_STARTED,
    EVENT_SCHEDULER_SHUTDOWN,
    EVENT_SCHEDULER_PAUSED,
)
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask import Flask, render_template

from jobs import api
from jobs.extensions import scheduler
from jobs.result_jobstore import ResultJobStore
from gptengine.core.common_util import write_job_flag
from gptengine.settings import JOB_STORE


# logger = logging.getLogger("root")
logger = logging.getLogger()


# print(__name__)


# def test_job():
#     train_word2vec_model


def build_app():
    app = Flask(__name__)
    from gptengine.views.admin import admin

    app.register_blueprint(admin)

    from gptengine.api.v1 import api as api_1_0_blueprint

    app.register_blueprint(api_1_0_blueprint, url_prefix="/api/v1")
    return app


def create_app(config_object="jobs.settings"):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_logging(app)
    register_extensions(app)
    register_blueprints(app)

    # register_errorhandlers(app)
    # register_shellcontext(app)
    # register_commands(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    # bcrypt.init_app(app)
    # cache.init_app(app)
    # db.init_app(app)
    # csrf_protect.init_app(app)
    # login_manager.init_app(app)
    # debug_toolbar.init_app(app)
    # migrate.init_app(app, db)
    # webpack.init_app(app)
    app.config.update(
        {
            "SCHEDULER_JOBSTORES": {
                "default": SQLAlchemyJobStore(url="sqlite:///jobs.sqlite")
            }
        }
    )

    # str=codecs.open("/tmp/flag",'r','utf-8').read().strip("\n")
    # if str == "0":
    #     app.config.update(
    #
    #         {"SCHEDULER_EXECUTORS": {
    #             'default':ThreadPoolExecutor(20)
    #             # 'default': ProcessPoolExecutor(20),
    #         }})
    # else:
    app.config.update(
        {
            "SCHEDULER_EXECUTORS": {
                # 'default':ThreadPoolExecutor(20)
                "default": ProcessPoolExecutor(4)
            }
        }
    )

    app.config.update(
        {"SCHEDULER_JOB_DEFAULTS": {"coalesce": False, "max_instances": 20}}
    )

    scheduler.init_app(app)
    scheduler._add_url_route(
        "job_result", "/jobs/<job_id>/result", api.get_job_result, "GET"
    )

    #
    # scheduler.add_listener(my_listener,EVENT_ALL)
    scheduler.add_listener(my_listener, EVENT_ALL)
    # scheduler.add_listener(my_listener,(EVENT_JOB_ADDED |
    #                                     EVENT_JOB_REMOVED |
    #                                     EVENT_JOB_MODIFIED |
    #                                     EVENT_JOB_EXECUTED |
    #                                     EVENT_JOB_ERROR |
    #                                     EVENT_JOB_MISSED))
    return None


def my_listener(events):
    resultworker = ResultJobStore(url=JOB_STORE)
    if events.code == EVENT_JOB_ADDED:
        # logger.info ("Job %s has ADDED ." % str(events.job_id))
        write_job_flag(events.job_id, "EVENT_JOB_ADDED")
        logger.info("Job %s has ADDED ." % str(events.job_id))
        resultworker.add_job_status(events.job_id, {"job_status": "EVENT_JOB_ADDED"})
    elif events.code == EVENT_JOB_REMOVED:
        # write_job_flag(events.job_id, 'EVENT_JOB_RUNNING')
        logger.info("Job %s has EVENT_JOB_RUNNING ." % str(events.job_id))
        resultworker.update_job_status(
            events.job_id, {"job_status": "EVENT_JOB_RUNNING"}
        )
        logger.info("Job %s has EVENT_JOB_RUNNING ." % str(events.job_id))
    elif events.code == EVENT_JOB_MODIFIED:
        # write_job_flag(events.job_id, 'EVENT_JOB_MODIFIED')
        resultworker.update_job_status(
            events.job_id, {"job_status": "EVENT_JOB_MODIFIED"}
        )
        logger.error("Job %s has EVENT_JOB_MODIFIED." % str(events.job_id))
    elif events.code == EVENT_JOB_EXECUTED:
        # write_job_flag(events.job_id, 'EVENT_JOB_EXECUTED')
        resultworker.update_job_status(
            events.job_id, {"job_status": " EVENT_JOB_EXECUTED"}
        )
        logger.info("!!!!!Job %s has EVENT_JOB_EXECUTED ." % str(events.job_id))
    elif events.code == EVENT_JOB_ERROR:
        resultworker.update_job_status(events.job_id, {"job_status": "EVENT_JOB_ERROR"})
        logger.error(events.exception)
        logger.error("Job %s has EVENT_JOB_ERROR." % str(events.job_id))
    elif events.code == EVENT_JOB_MISSED:
        # write_job_flag(events.job_id, 'EVENT_JOB_MISSED')
        resultworker.update_job_status(
            events.job_id, {"job_status": "EVENT_JOB_MISSED"}
        )
        logger.warning("Job %s has EVENT_JOB_MISSED." % str(events.job_id))
    # elif events.code == EVENT_JOB_SUBMITTED:
    #     write_job_flag(events.job_id,'EVENT_JOB_SUBMITTED')
    #     print ("Job %s has EVENT_JOB_SUBMITTED." % str(events.job_id))
    elif events.code == EVENT_JOB_MAX_INSTANCES:
        write_job_flag(events.job_id, "EVENT_JOB_MAX_INSTANCES")
        logger.error("Job %s has EVENT_JOB_MAX_INSTANCES." % str(events.job_id))
    elif events.code == EVENT_EXECUTOR_ADDED:
        write_job_flag(events.job_id, "EVENT_EXECUTOR_ADDED")
        logger.info("Job %s has EVENT_EXECUTOR_ADDED." % str(events.job_id))
    elif events.code == EVENT_SCHEDULER_RESUMED:
        write_job_flag(events.job_id, "EVENT_SCHEDULER_RESUMED")
        logger.info("Job %s has EVENT_EXECUTOR_ADDED." % str(events.job_id))
    elif events.code == EVENT_SCHEDULER_PAUSED:
        write_job_flag(events.job_id, "EVENT_SCHEDULER_PAUSED")
        logger.info("Job %s has EVENT_SCHEDULER_PAUSED." % str(events.job_id))
    elif events.code == EVENT_SCHEDULER_SHUTDOWN:
        write_job_flag(events.job_id, "EVENT_SCHEDULER_SHUTDOWN")
        logger.info("Job %s has EVENT_SCHEDULER_SHUTDOWN." % str(events.job_id))
    elif events.code == EVENT_SCHEDULER_STARTED:
        write_job_flag(events.job_id, "EVENT_SCHEDULER_STARTED")
        logger.info("Job %s has EVENT_SCHEDULER_STARTED." % str(events.job_id))
    else:
        logger.info("Job %s code %d." % str(events.job_id, events.code))
    # elif events.code == :
    #     print ("Job %s has error." % str(events.job_id))


# def my_listener(event):
#     if event.exception:
#         print('The job crashed')
#     else:
#         print('The job worked')


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error templates."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template("{0}.html".format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_logging(app):
    abspath = os.path.abspath(os.path.dirname(__file__))
    fileConfig(os.path.join(abspath, "./logging_config.ini"))

    # logger = logging.getLogger('thesis_train')
    # app.logger.setLevel(logging.DEBUG)  # 日志模块等级,优先级最大


def register_blueprints(app):
    """Register Flask blueBackgroundSchedulerprints."""
    # app.register_blueprint(public.views.blueprint)
    # app.register_blueprint(user.views.blueprint)
    # from gptengine.views.admin import admin
    # app.register_blueprint(admin)
    #
    # # from api.v1.resources.index import api
    # # app.register_blueprint(api, url_prefix='/api/v1/index')
    #
    # from gptengine.api.v1 import api as api_1_0_blueprint
    # app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1')

    # from gptengine.user.index import admin
    # app.register_blueprint(admin)

    return None


# app = build_app()
app = create_app()
if __name__ == "__main__":
    # Only for debugging while developing
    scheduler.start()
    app.run(host="0.0.0.0", debug=False, port=8889)
