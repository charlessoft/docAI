# -*- coding: utf-8 -*-
from jobs.result_jobstore import ResultJobStore


class TestResultJobstore(object):
    url = "sqlite:////tmp/jobs.sqlite"

    def add_job_result(self):
        ResultJobStore(url=self.url).add_job_result(
            {"job_id": "xxxaaa", "job_result": "aaaaaa"}
        )

    def lookup_job_result(self):
        ret = ResultJobStore(url=self.url).lookup_job("xxx")
        print(ret["job_id"])

    def update_job_result(self):

        update_dic = {"job_id": "xxxaaa", "job_result": "hello11111 world"}

        print(ResultJobStore(url=self.url).update_job_result(update_dic))


if __name__ == "__main__":
    # TestResultJobstore().add_job_result()
    TestResultJobstore().update_job_result()
