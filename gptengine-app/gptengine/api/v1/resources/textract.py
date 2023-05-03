# -*- coding: utf-8 -*-
from flask import current_app as app, request

from pdf2image.api.v1 import api, restful
from pdf2image.common_utils import get_cache_path, remove_tmp_file
from pdf2image.core import jobmgr
from pdf2image.core.textract.parsers import pdf_parser


@api.route("/textract_status", methods=["GET"])
def word2vec():
    """
       获取模型训练状态
       ---
       tags:
         - textract
       consumes:
         - application/json
       produces:
         - application/json
       parameters:
          - in: body
            name: body
            description: 获取抽取状态
            required: true
            schema:
                type: string
                properties:
                    model_id:
                        type: string
                        example: "textract_id"
                        description: 模型id
       responses:
         200:
           description: successful operation
           schema:
            type: object
            properties:
              model_id:
                type: string
                example: "textract_id"
              status:
                type: string
                example: EVENT_JOB_EXECUTED

         400:
           description: Invalid ID supplied
         404:
          description: Page not found
         405:
          description: Validation exception
    """
    id = request.args.get("model_id", None)
    if id:
        strs = jobmgr.read_job_flag(id)
        return restful.success(data={"status": strs})
        # return strs
    else:
        return restful.params_error("required invalid! missing model_id")
        # return 'required invalid! missing model_id', 400


@api.route("/textract", methods=["POST"])
def textract():
    """
        抽取文本
        ---
        tags:
          - textract
        produces:
         - application/json
        parameters:
          - in: formData
            name: file
            type: file
            required: true
            description: 待抽取文件
          - in: formData
            name: type
            type: string
            required: true
            example: "pdf/word"
            description: 文件类型.

        responses:
          200:
            description: successful operation
            example: "running ok!"
     """
    app.logger.info("ner.req")

    parser = pdf_parser.Parser()

    if "type" not in request.form:
        return restful.params_error("required invalid! missing type")
    filetype = request.form["type"]

    file_name = "%s.%s" % (get_cache_path(), filetype)
    file = request.files["file"]
    file.save(file_name)

    if filetype.lower() == "pdf":
        content = bytes.decode(parser.extract(file_name))
        remove_tmp_file(file_name)
        return restful.success(data={"content": content})
    else:
        return restful.params_error("no impl %s" % (filetype))
