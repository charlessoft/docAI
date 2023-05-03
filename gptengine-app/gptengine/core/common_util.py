#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: chenjianghai
# @Date:   2018-08-21
import codecs
import os
import pickle  # pickle模块
import random
import re
import time

from gptengine.settings import TEXTMINER_ROOT_FOLDER

sentence_end_tok = "。？…！!?"


def cut_words(sentence, impl="jieba", stopwords=[]):
    """
    分词，支持jieba,ltp.默认采用jieba分词.
    :param sentence:
    :return:
    """
    if impl.__eq__(jieba):
        sentence = clean_text(sentence)
        # print("清洗后：" + sentence)
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        if len(stopwords) == 0:
            stopword_path = os.path.dirname(cur_dir)
            stopword_path = os.path.join(stopword_path, "resources/stop_word.dic")
            stopwords = load_stopwords(stopword_path)
            if len(stopwords) == 0:
                print("cut_words.stop.word.empty ,please check")
        return filter(lambda x: not stopwords.__contains__(x), jieba.cut(sentence))
    else:
        return []


def postag(sentence, impl="jieba"):
    if impl.__eq__(jieba):
        sentence = clean_text(sentence)
        words = pseg.cut(sentence)
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        stopword_path = os.path.dirname(cur_dir)
        stopword_path = os.path.join(stopword_path, "resources/stop_word.dic")
        stopwords = load_stopwords(stopword_path)
        if len(stopwords) == 0:
            print("postag.stop.word.empty ,please check")
        return filter(lambda x: not stopwords.__contains__(x.word), words)
    else:
        return []


def clean_text(text):
    """
    Clean raw text:
    1. strip
    2. remove url
    3. remove html tags: e.g. <div> <p>
    4. shorten consecutive white chars: " \t\r\n" => " "
    5. replace consecutive eos tokens => "。"
    6. make each text ends with a "。"

    Args:
        text: str

    Returns:
        preprocessed text: str
    """
    text = text.replace(" ", "")
    text = text.replace("\n", "")
    text = text.replace("\r", "")
    if not isinstance(text, str):
        try:
            text = str(text)
        except TypeError:
            text = ""
    text = text.strip()
    sentences = re.split(r"[{}]".format(sentence_end_tok), text)
    text = "。".join([s for s in sentences if len(s) > 0])
    # add <EOS> for each doc
    if len(text) > 0:
        text += "。"
    else:
        text = ""
    return text


def load_stopwords(path=""):
    """
    加载停用词
    :param path:
    :return:
    """
    if path == "":
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.dirname(cur_dir)
        path = os.path.join(path, "resources/stop_word.dic")

    with open(path, "r", encoding="UTF-8") as f:
        stopwords = filter(lambda x: x, map(lambda x: x.strip(), f.readlines()))
    # for word in stopwords:
    #    print(word)
    return frozenset(stopwords)


def get_pos_model_path():
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.dirname(cur_dir)
    return os.path.join(path, "resources/ltp_data_v3.4.0/pos.model")


def get_ner_model_path():
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.dirname(cur_dir)
    return os.path.join(path, "resources/ltp_data_v3.4.0/ner.model")


def cut_sentence(sentence):
    """
    分句
    :param sentence:
    :return:
    """
    sentence = clean_text(sentence)
    delimiters = frozenset(sentence_end_tok)
    buf = []
    for ch in sentence:
        buf.append(ch)
        if delimiters.__contains__(ch):
            yield "".join(buf)
            buf = []
    if buf:
        yield "".join(buf)


def get_resource_path(sub_path=""):
    """
    获取统一资源路径
    :param sub_path:
    :return:
    """
    if sub_path:
        return os.path.join(TEXTMINER_ROOT_FOLDER, "gptengine", "resources", sub_path)
    return os.path.join(TEXTMINER_ROOT_FOLDER, "gptengine", "resources")


def get_cache_path_ex(sub_name=""):
    if sub_name:
        return os.path.join(TEXTMINER_ROOT_FOLDER, "gptengine", "cache", sub_name)
    return os.path.join(TEXTMINER_ROOT_FOLDER, "gptengine", "cache")

def get_cache_exls_path():
    return os.path.join(get_cache_path_ex(),str(time.time()) + "_" + str(random.randint(1000, 9999)) +".xlsx")

def get_cache_path():
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.dirname(cur_dir)
    return os.path.join(
        path,
        "cache/" + str(time.time()) + "_" + str(random.randint(1000, 9999)) + ".tmp",
    )


def write_job_flag(job_id, flag):
    try:
        codecs.open("/tmp/testjob/" + job_id, "a", "utf-8").write("%s\n" % (flag))
    except Exception as e:
        print(e)


def read_job_flag(job_id):
    return codecs.open("/tmp/" + job_id, "r", "utf-8").read()


def save_model(file_path, clf):
    with open(file_path, "wb") as f:
        pickle.dump(clf, f)


# 读取Model
# with open('save/clf.pickle', 'rb') as f:
#     clf2 = pickle.load(f)
#     #测试读取后的Model
#     print(clf2.predict(X[0:1]))


def load_model(file_path):
    with open(file_path, "rb") as f:
        clf = pickle.load(f)
    return clf


if __name__ == "__main__":
    # jieba.add_word("江大桥", freq=200000, tag=None)
    jieba.suggest_freq("江大桥", tune=True)
    print("/".join(jieba.cut("江州市长江大桥参加了长江大桥的通车仪式。")))
