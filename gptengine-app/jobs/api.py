# -*- coding: utf-8 -*-
import logging
import traceback

from flask import jsonify

from jobs.result_jobstore import ResultJobStore
from gptengine.settings import JOB_STORE

logger = logging.getLogger()


def get_job_result(job_id):
    """get a job Result."""
    try:
        logger.info("JOB_STORE: %s, job_id:%s" % (JOB_STORE, job_id))
        resltworker = ResultJobStore(JOB_STORE)
        result = resltworker.lookup_job(job_id)

        if not result:
            return jsonify(dict(error_message="Job %s not found" % job_id)), 404
        ret = dict(result)
        del ret["create_time"]
        del ret["update_time"]
        # ret = {'job_id':"xx","job_result":"fffff"}
        logger.info(ret)
        return jsonify(ret)
    except Exception as e:
        exstr = traceback.format_exc()
        logger.error(exstr)
        logger.error(e)
        return jsonify(dict(error_message="Job %s result error" % job_id)), 400
