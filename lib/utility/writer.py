#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 保存结果到文件

from lib.utility.path import *


def write_urls_to_file(file_name, urls):
    file_name = DATA_PATH + "/" + file_name
    txt_file = open(file_name, 'w')
    for url in urls:
        txt_file.write(url+"\n")
    txt_file.close()
