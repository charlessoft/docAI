# -*- coding: utf-8 -*-
import codecs
import datetime
import logging
import os
import threading
import time

from jobs.result_jobstore import ResultJobStore
from jobs.settings import JOB_STORE

logger = logging.getLogger()


def update_job_result(job_id, result):
    resultworker = ResultJobStore(url=JOB_STORE)
    job_result = resultworker.lookup_job(job_id)
    print(job_result)
    if job_result:
        resultworker.update_job_result(job_id, result)
    else:
        resultworker.add_job_result(job_id, result)


def echo_for_test(job_id, args):
    print("========job========")
    print(
        "%s,echo_for_test job thread_id-%d, process_id-%d,%s\n"
        % (job_id, threading.get_ident(), os.getpid(), str(args))
    )
    print(JOB_STORE)
    ret = {"job_result": {"success": True, "result": {}}}
    # resultworker = ResultJobStore(url=JOB_STORE)
    update_job_result(job_id, ret)
    print("========job======== end...")
    # job_result = resultworker.lookup_job(job_id)
    # print(job_result)
    # if job_result:
    #     resultworker.update_job_result(job_id, ret)
    # else:
    #     resultworker.add_job_result(job_id, ret)


def test_write_for_benchmark(job_id, args):
    """
    for benchmark
    :param args:
    :return:
    """
    print(
        "echo_for_test job thread_id-%d, process_id-%d,%s\n"
        % (threading.get_ident(), os.getpid(), str(args))
    )
    return

    if args == "0":
        folder = "/tmp/asplogs/thread"
    else:
        folder = "/tmp/asplogs/process"
    if not os.path.exists(folder):
        os.makedirs(folder)
    thread_id = threading.get_ident()
    pid = os.getpid()
    i = 0
    start = time.time()
    while True:
        i += 1
        if i > 1000000:
            break
        curtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        strs = "add_job job thread_id-%d, process_id-%d,%s\n" % (
            threading.get_ident(),
            os.getpid(),
            curtime,
        )
        print(strs)
        f = codecs.open(
            os.path.join(folder, "%d-%d.txt" % (pid, thread_id)), "a", "utf-8"
        )
        f.write(strs)
        f.close()
    end = time.time()
    left = end - start
    f = codecs.open(os.path.join(folder, "total.txt"), "a", "utf-8")
    f.write("pid=%d,thread_id=%d, left:%d\n" % (pid, thread_id, left))
    f.close()
    os.system('sh /tmp/dding "study %s"' % ("okkkkk"))


def test_job_by_args(arg):
    print(
        "test_job_by_args job thread_id-{0}, process_id-{1},{2}".format(
            threading.get_ident(), os.getpid(), arg
        )
    )
    time.sleep(50)


def add_job():
    print(
        "add_job job thread_id-{0}, process_id-{1}".format(
            threading.get_ident(), os.getpid()
        )
    )
    time.sleep(50)


def aps_train_word2vec_model(new_word_list, sentences_list, model_id):
    print("====")
    logger.info("==ad=ad=ad=ad=a=dad")
    logger.info(model_id)
    print(model_id)
    print("====")
    # time.sleep(5)

    #
    # af = codecs.open("/tmp/ccc.txt", 'a', 'utf-8')
    # now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print(now_time)
    # af.write('pid=%s,%s,hello:%s\n' % (os.getpid(), now_time,model_id))
    # af.write("aps_train_word2vec_model\n")
    # af.close()

    # raise Exception("FFA")
    # init_word2vec_dict(new_word_list)
    # train_word2vec_model(sentences_list,model_id)

    # train_word2vec_model()


# print(__name__)
