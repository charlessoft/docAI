# -*- coding: utf-8 -*-
import codecs

import requests
from flask import current_app as app


def write_job_flag(job_id, flag):
    try:
        codecs.open('/tmp/' + job_id, 'w', 'utf-8').write('%s\n' % (flag))
    except Exception as e:
        print(e)


def read_job_flag(job_id):
    return codecs.open('/tmp/' + job_id, 'r', 'utf-8').read()

def run_job(**kwargs):

    # dic = {}
    # dic['id'] = model_id
    # # dic['func'] = 'textminer.api.v1.job.job:aps_train_word2vec_model'
    # dic['func'] = 'jobs.job:aps_train_word2vec_model'
    # dic['args'] = [sentences_list, model_id]

    r = requests.post('%s/scheduler/jobs' % (app.config['JOB_URL']), json=kwargs)
    return r.status_code


def job_callback(**kwargs):
    r = requests.post(kwargs['url'],json=kwargs)
