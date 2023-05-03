# -*- coding: utf-8 -*-
import datetime
from uuid import uuid4

import requests


class TestJob(object):
    url = "http://localhost:8889/scheduler"
    job_id = "xxxxxxxxxx"

    #
    def test_get_jobs(self):
        test_url = self.url + "/jobs"
        r = requests.get(test_url)
        print(r.json())
        assert 200 == r.status_code

    # assert r.json()

    def test_add_job(self):
        """
        增加job, 间隔十秒
        :return:
        """
        test_url = self.url + "/jobs"

        job = {
            "id": self.job_id,  # 任务的唯一ID，不要冲突
            "func": "job:add_job",  # 执行任务的function名称 # 服务启动根路径下job文件
            "args": "",  # 如果function需要参数，就在这里添加
            "trigger": "interval",
            "seconds": 10,
        }
        r = requests.post(test_url, json=job)
        print(r.content)
        assert 200 == r.status_code
        return r.json()

    def test_add_job_interval(self):
        test_url = self.url + "/jobs"

        job = {
            "id": uuid4().hex,  # 任务的唯一ID，不要冲突
            "func": "job:add_job",  # 执行任务的function名称 # 服务启动根路径下job文件
            "trigger": "interval",
            "seconds": 10,
            # 'args': ['args..args..'],  # 如果function需要参数，就在这里添加
        }
        r = requests.post(test_url, json=job)
        print(r.content)
        assert 200 == r.status_code
        return r.json()

    def test_update_job_interval(self):
        test_url = self.url + "/jobs/%s" % (self.job_id)

        job = {
            "func": "job:test_job_by_args",  # 执行任务的function名称 # 服务启动根路径下job文件
            "trigger": "interval",
            "seconds": 5,
            "args": ("test .......",),  # 如果function需要参数，就在这里添加
        }
        print(job)
        r = requests.patch(test_url, json=job)
        print(r.content)
        assert 200 == r.status_code

    def test_pause_job(self):
        test_url = self.url + "/jobs/%s/pause" % (self.job_id)

        # job = {
        #
        #     'func': 'job:test_job_by_args',  # 执行任务的function名称 # 服务启动根路径下job文件
        #     'trigger': 'interval',
        #     'seconds': 5,
        #     'args': ('test .......',),  # 如果function需要参数，就在这里添加
        # }
        r = requests.post(test_url)
        print(r.content)
        assert 200 == r.status_code

    def test_add_job_once(self):
        test_url = self.url + "/jobs"
        # strs=codecs.open("/tmp/flag",'r','utf-8').read().strip("\n")
        # print()
        # assert strs == "0"
        # assert False

        for idx in range(1):
            job_id = uuid4().hex
            job = {
                "id": job_id,
                "trigger": "date",
                "run_date": (
                    datetime.datetime.now() + datetime.timedelta(seconds=5)
                ).strftime("%Y-%m-%d %H:%M:%S"),
                "func": "job:echo_for_test",  # 执行任务的function名称 # 服务启动根路径下job文件
                "args": [job_id, "ddd"],  # 如果function需要参数，就在这里添加
            }
            r = requests.post(test_url, json=job)
            print(r.content)
            assert 200 == r.status_code
        # job = {
        #     "id":uuid1().hex,
        #     'func': 'job:test_write',  # 执行任务的function名称 # 服务启动根路径下job文件
        #     'args':[strs]# 如果function需要参数，就在这里添加
        # }
        # r = requests.post(test_url,json=job)
        #

    def test_delete_job(self):
        dic = self.test_add_job_interval()
        print(dic)
        test_url = self.url + "/jobs/%s" % (dic["id"])

        r = requests.delete(test_url)
        print(r.content)
        assert 204 == r.status_code


# if __name__ == "__main__":
#     TestJob().test_add_job_once()
# TestJob().test_update_job_interval()


#     self._add_url_route('get_scheduler_info', '', api.get_scheduler_info, 'GET')
# self._add_url_route('add_job', TestJob'/jobs', api.add_job, 'POST')
# self._add_url_route('get_job', '/jobs/<job_id>', api.get_job, 'GET')
# self._add_url_route('get_jobs', '/jobs', api.get_jobs, 'GET')
# self._add_url_route('delete_job', '/jobs/<job_id>', api.delete_job, 'DELETE')
# self._add_url_route('update_job', '/jobs/<job_id>', api.update_job, 'PATCH')
# self._add_url_route('pause_job', '/jobs/<job_id>/pause', api.pause_job, 'POST')
# self._add_url_route('resume_job', '/jobs/<job_id>/resume', api.resume_job, 'POST')
# self._add_url_route('run_job', '/jobs/<job_id>/run', api.run_job, 'POST')
