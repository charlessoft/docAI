# -*- coding: utf-8 -*-
# from pdf2image.core.textract.parsers import pdf_parser
import os

from pdftohtml.core.convert import pdf_parser


def test_pdf():
    test_file = '/Users/charles/Desktop/基础环境部署.pdf'
    parser=pdf_parser.Parser()
    bres=parser.convert(test_file)
    # bres = True
    if bres:
        print('success', test_file[:-4]+'.html')
    else:
        print("fail")
    # print(bytes.decode(b))
    # return bytes.decode(b)
    # print(bytes.decode(b))

if __name__ == '__main__':
    test_pdf()
