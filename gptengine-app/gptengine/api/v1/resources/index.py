# -*- coding: utf-8 -*-
import datetime
import os
import re
import uuid

import joblib
import requests
from flask import current_app as app, request
from langchain import PromptTemplate
from pyquery import PyQuery as pq

from gptengine.api.v1 import api
from gptengine.core.common_util import get_resource_path
from gptengine.core.newAzureOpenAI import NewAzureOpenAI
from gptengine.core.utils import calc_cos_similarity
from gptengine.libs import restful
import openai

openai.api_type = "azure"
openai.api_base = "https://adt-openai.openai.azure.com/"
# openai.api_version = "2022-12-01"
openai.api_version = "2023-03-15-preview"
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY", 'azure openai key')
from langchain.chains.conversation.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.chains import ConversationChain

GLOBAL = {}

def QueryVector(question):
    user_query_response = openai.Embedding.create(
        input=question,
        engine="text-embedding-ada-002"
    )
    user_query_embedding = user_query_response['data'][0]['embedding']
    pkl = get_resource_path('text_embeddings.pkl')
    text_embeddings = joblib.load(pkl)

    # 计算用户问题和每个段落的相似度，取相似度最高的几个段落，和用户的问题一起送入chatgpt
    related_paragraph = calc_cos_similarity(text_embeddings, user_query_embedding)
    print(f"最相关的章节为:{related_paragraph}")
    reference_content = ""
    for item in related_paragraph:
        reference_content += text_embeddings[item]['content']
    context = reference_content
    return context


@api.route('/echo')
def health():
    """
        ping->pong
        ---
        tags:
          - health
        produces:
         - application/json
        responses:
          200:
            description: successful operation
            example: "running ok!"
     """
    return restful.success()
    # user = User.query.get_or_404(1)
    # return restful.success("gptengine running ok")

@api.route("/getcorpuslist",methods=['GET'])
def listcopus():
    pkl = get_resource_path('text_embeddings.pkl')

    text_embeddings = joblib.load(pkl)
    return restful.success(data=text_embeddings)


@api.route("/delcorpusIds",methods=['POST'])
def delcorpusIds():
    print(request)
    dic = request.json
    pkl = get_resource_path('text_embeddings.pkl')
    text_embeddings = joblib.load(pkl)
    for id in dic['ids']:
        print(id)
        print(text_embeddings[id])
        del text_embeddings[id]
    joblib.dump(text_embeddings,pkl)
    return restful.success('ok')
#
@api.route('/delcorpus',methods=['POST'])
def delcorpus():
    print(request)
    return restful.success('ok')


@api.route("/addcorpus",methods=['POST'])
def addcorpus():
    file = request.files['file']
    text_content = file.read().decode('utf-8')

# dic = request.json
    id = str(datetime.datetime.today().date())+'_'+str(uuid.uuid1())
    # text_content = dic['content']
    openai.api_version = "2022-12-01"
    pkl = get_resource_path('text_embeddings.pkl')

    text_embeddings = joblib.load(pkl)


    response = openai.Embedding.create(
        input=text_content,
        engine="text-embedding-ada-002"
    )
    text_embeddings[id] = {'embedding': response['data'][0]['embedding'], 'content': text_content}
    joblib.dump(text_embeddings, pkl)
    return restful.success('ok')

    # text_embeddings[text_name] = {'embedding': response['data'][0]['embedding'], 'content': text_content}
    # engine = dic.get('engine', 'ChatGPT-0301')
    # sysrole = dic['system']
    # question = dic['question']
    # context = dic['context']
@api.route('/memerychat_raw', methods=["POST"])
def memerychat_raw():
    dic = request.json
    chatId = dic['chatId']
    question = dic['question']
    sysrole = dic.get('system','You are Foxiter, working on Foxit as a senior C++ developer\n')
    engine = dic.get('engine', 'ChatGPT-0301')
    # sysrole = dic['system']
    # first_query = dic['first_query']

    content = QueryVector(question)
    # mem = ConversationBufferMemory()

    mem = None
    # if chatId in GLOBAL:
    #     mem = GLOBAL[chatId]
    # else:
    #     mem = ConversationBufferMemory()
    #     GLOBAL[chatId] = mem
    # if len(content)!=0:
    #     mem.chat_memory.add_user_message(content)
    if chatId in GLOBAL:
        messages = GLOBAL[chatId]
        user  = {
            "role": "user",
            "content":"""${query}"""
        }

        user['content'] = user['content'].replace("${query}",question)
        messages.append( user)
        GLOBAL[chatId] =messages
    else:
        messages = [
                {
                    "role": "system",
                    "content": sysrole
                },
                {
                    "role": "user",
                    # "content": "根据上下文回答问题:\n " + context + "\n  问题:\n" + question
                    "content":"""CONTEXT:
${contextText}
USER QUESTION:
${query}
                    """
                },

            ]
        # content = QueryVector(question)

        messages[1]['content'] = messages[1]['content'].replace('${contextText}',content).replace('${query}',question)

        GLOBAL[chatId] = messages

    openai.api_version = "2023-03-15-preview"
    response = openai.ChatCompletion.create(
        engine=engine,
        messages=messages,
        # messages=[
        #     {
        #         "role": "system",
        #         "content": "You are an AI assistant that helps people find information."
        #     },
        #     {
        #         "role": "user",
        #         "content": "根据上下文回答问题:\n对所有的pdf文档操作,必须要打开文档,打开文档的函数是openpdf,\n 最终关闭文档, 关闭文档的函数是closepdf\n 获取pdf页面总数的函数是getpageCount.\n 添加annot的函数是addpdfannot\n  问题:\n 编写获取页面"
        #     },
        #     {"role":"assistant","content":""}
        # ],
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)
    #
    aicontent = response['choices'][0]['message']['content']
    GLOBAL[chatId].append({"role": "assistant", "content": aicontent})
    print(response)

    # data = {'raw_gpt_response': response,
    #         'answer': response['choices'][0]['message']['content'],
    #         'raw_message':messages,
    #         }
    data = {
        'answer':response['choices'][0]['message']['content']
    }
    return restful.success(data=data)



@api.route('/memerychat', methods=["POST"])
def memerychat():
    dic = request.json
    chatId = dic['chatId']
    question = dic['question']
    engine = dic.get('engine', 'ChatGPT-0301')
    # sysrole = dic['system']
    # first_query = dic['first_query']

    content = QueryVector(question)
    # mem = ConversationBufferMemory()

    mem = None
    if chatId in GLOBAL:
        mem = GLOBAL[chatId]
    else:
        mem = ConversationBufferMemory()
        GLOBAL[chatId] = mem
    if len(content)!=0:
        mem.chat_memory.add_user_message(content)


    llm = NewAzureOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY", openai.api_key),
        engine="ChatGPT-0301",
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None

    )
    prompt_template = """You are Foxiter, working on Foxit as a senior C++ developer. The AI is talkative and provides lots of specific details from its context. 

Current conversation:
{history}
Human: {input} <|im_end|>
AI:"""
    prompt_template = PromptTemplate(
        input_variables=["history", "input"],
        template=prompt_template
    )
    chain = ConversationChain(llm=llm, memory=mem,prompt=prompt_template)
    s = chain.run(question)
    print(s)
    return restful.success(data=s)





@api.route('/querysimilarity', methods=["POST"])
def querysimilarity():
    openai.api_version = "2022-12-01"

    dic = request.json
    question = dic.get('question')
    engine = dic.get('engine', 'ChatGPT-0301')
    sysrole = dic['system']
    # question = dic['question']
    # context =  dic['context']
    user_query_response = openai.Embedding.create(
        input=question,
        engine="text-embedding-ada-002"
    )
    user_query_embedding = user_query_response['data'][0]['embedding']
    pkl = get_resource_path('text_embeddings.pkl')
    text_embeddings = joblib.load(pkl)

    # 计算用户问题和每个段落的相似度，取相似度最高的几个段落，和用户的问题一起送入chatgpt
    related_paragraph = calc_cos_similarity(text_embeddings, user_query_embedding)
    print(f"最相关的章节为:{related_paragraph}")
    reference_content = ""
    for item in related_paragraph:
        reference_content += text_embeddings[item]['content']
    context = reference_content
    openai.api_version = "2023-03-15-preview"

    messages = [
        {
            "role": "system",
            "content": sysrole
        },
        {
            "role": "user",
            # "content": "根据上下文回答问题:\n " + context + "\n  问题:\n" + question
            "content":"""CONTEXT:
${contextText}
USER QUESTION: 
${query}
            """
        },
        {"role": "assistant", "content": ""}
    ]
    messages[1]['content'] = messages[1]['content'].replace('${contextText}',context).replace('${query}',question)
    response = openai.ChatCompletion.create(
        engine=engine,
        messages=messages,
        # messages=[
        #     {
        #         "role": "system",
        #         "content": "You are an AI assistant that helps people find information."
        #     },
        #     {
        #         "role": "user",
        #         "content": "根据上下文回答问题:\n对所有的pdf文档操作,必须要打开文档,打开文档的函数是openpdf,\n 最终关闭文档, 关闭文档的函数是closepdf\n 获取pdf页面总数的函数是getpageCount.\n 添加annot的函数是addpdfannot\n  问题:\n 编写获取页面"
        #     },
        #     {"role":"assistant","content":""}
        # ],
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)
    print(response['choices'][0]['message']['content'])
    print(response)

    data = {'raw_gpt_response': response,
            'answer': response['choices'][0]['message']['content'],
            'similarity': str(related_paragraph) + '\n' + context,
            'raw_message':messages,
            }
    return restful.success(data=data)


@api.route('/testrole', methods=["POST"])
def testrole():
    dic = request.json
    engine = dic.get('engine', 'ChatGPT-0301')
    sysrole = dic['system']
    question = dic['question']
    context = dic['context']
    messages = [
        {
            "role": "system",
            "content": sysrole
        },
        {
            "role": "user",
            "content": "根据上下文回答问题:\n " + context + "\n  问题:\n" + question
        },
        {"role": "assistant", "content": ""}
    ],
    response = openai.ChatCompletion.create(
        engine=engine,
        messages=messages,
        # messages=[
        #     {
        #         "role": "system",
        #         "content": "You are an AI assistant that helps people find information."
        #     },
        #     {
        #         "role": "user",
        #         "content": "根据上下文回答问题:\n对所有的pdf文档操作,必须要打开文档,打开文档的函数是openpdf,\n 最终关闭文档, 关闭文档的函数是closepdf\n 获取pdf页面总数的函数是getpageCount.\n 添加annot的函数是addpdfannot\n  问题:\n 编写获取页面"
        #     },
        #     {"role":"assistant","content":""}
        # ],
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)
    print(response['choices'][0]['message']['content'])
    print(response)

    return restful.success(response['choices'][0]['message']['content'])


# @api_wrap.resource('/hello')                   #  Create a URL route to this resource
# class HelloWorld(Resource):            #  Create a RESTful resource
#     def get(self):                     #  Create GET endpoint
#         """
#         ping->pong
#         ---
#         tags:
#           - health
#         produces:
#          - application/json
#         responses:
#           200:
#             description: successful operation
#             example: "running ok!"
#         """
#         # parser = reqparse.RequestParser(bundle_errors=True)
#         # parser.add_argument('model_id', type=str, location=['form', 'json'], required=True, help="缺少model_id")
#         # req = parser.parse_args()
#         return {'hello': 'world'}


@api.route('/getaccountbiz', methods=["GET"])
def biz():
    """

    :return:
    """
    biz = ''
    url = request.args.get('url', None)
    if not url:
        return restful.params_error("url is null")
    app.logger.info("getaccountbiz.req")
    app.logger.info("url: %s" % (url))
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        pattent = "__biz=(.*?)&"
        m = re.search(pattent, r.text)
        if m:
            biz = m.groups()[0]
        else:
            return restful.params_error("未查询到biz")

        doc = pq(r.text)
        nickname = doc("#js_name").text()

        # account = Accounts.query.filter_by(biz=biz).first()
        # if account:
        #     return restful.success("账号已经存在")
        # else:
        #     accInfo = Accounts.create(nickname=nickname, biz=biz)
        #     accInfo.save()
    return restful.success()
