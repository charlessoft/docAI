# -*- coding: utf-8 -*-
import datetime
import logging
import os
import uuid

import requests

logger = logging.getLogger("job")


class JobMgr(object):
    def __init__(self, url=""):
        self.url = url or os.environ.get("JOBURL", "")

    def _post(self, url, job):
        ret = {"success": False, "data": [], "message": ""}

        try:
            logger.error(url)
            logger.info(url)
            logger.info(job)
            r = requests.post(url, json=job)
            if r.status_code == requests.codes.ok:
                ret["success"] = True

            ret["data"] = r.json()
            return ret
        except Exception as e:
            logger.error(e)
            ret["message"] = str(e)
            return ret

    def _put(self, url, job):
        pass

    def _get(self, url):
        ret = {"success": False, "data": [], "message": ""}
        try:
            r = requests.get(url)
            if r.status_code == requests.codes.ok:
                ret["success"] = True
            ret["data"] = r.json()
            return ret
        except Exception as e:
            logger.error(e)
            ret["message"] = str(e)
            return ret

    def _delete(self, url):
        ret = {"success": False, "data": [], "message": ""}
        try:
            r = requests.delete(url)
            if r.status_code == 204:
                ret["success"] = True
                return ret
            return ret
            # return {'delete':True}
            # return {'delete':False}
        except Exception as e:
            logger.error(e)
            ret["message"] = str(e)
            return ret

    def _patch(self, url, job):
        ret = {"success": False, "data": [], "message": ""}
        try:
            r = requests.patch(url, json=job)
            ret["success"] = True
            ret["data"] = r.json()
            return ret
        except Exception as e:
            logger.error(e)
            ret["message"] = e
            return ret

    def get_job(self, job_id):
        url = self.url + "/jobs/%s" % (job_id)
        return self._get(url)

    def get_jobs(self):
        url = self.url + "/jobs"
        return self._get(url)

    def delete_job(self, job_id):
        url = self.url + "/jobs/%s" % (job_id)
        return self._delete(url)

    def update_job(self, id, func, args, **kwargs):
        url = self.url + "/jobs/%s" % (id)
        logger.info(url)
        job = {"func": func}
        if args:
            job.update({"args": args})
        job.update(kwargs)
        logger.info(job)
        return self._patch(url, job)

    def get_job_result(self, job_id):
        logger.info("get_job_result")
        url = self.url + "/jobs/%s/result" % (job_id)
        return self._get(url)

    def add_job(self, job_id="", func="", args=[], **kwargs):
        """
        add job,
        :param func: job:xxx函数
        :param args:
        :param kwargs:
        :return: dict
        {
            'success': True,
            'data': {
                'id': 'a1cfe93c9dd24c32adbdc94c21003e2e',
                'name': 'a1cfe93c9dd24c32adbdc94c21003e2e',
                'func': 'job:echo_for_test',
                'args': ['1234'],
                'kwargs': {},
                'trigger': 'date',
                'run_date': '2019-02-19T09:10:41.130758+08:00',
                'misfire_grace_time': 1,
                'max_instances': 20,
                'next_run_time': '2019-02-19T09:10:41.130758+08:00'
            },
            'message': ''
        }
        """
        logger.info("add_job")
        # id= uuid.uuid4().hex

        # 默认推迟5秒执行
        trigger = {
            "trigger": "date",
            "run_date": (
                datetime.datetime.now() + datetime.timedelta(seconds=5)
            ).strftime("%Y-%m-%d %H:%M:%S"),
        }
        job_id = job_id or uuid.uuid4().hex
        job = {
            # 'id': 'rds-to-mysql-1',  # 任务的唯一ID，不要冲突
            # 'func': 'job:add_job',  # 执行任务的function名称 # 服务启动根路径下job文件
            # 'args': '',  # 如果function需要参数，就在这里添加
            "id": job_id,
            "func": func,
        }
        # job_id 必须是第一个参数
        args.insert(0, job_id)  # 在执行任务重保留任务id,记录到数据库表中
        job.update({"args": args})
        job.update(kwargs)

        if "trigger" not in job:
            job.update(trigger)

        logger.info(job)
        url = self.url + "/jobs"
        logger.info(url)
        return self._post(url, job)
