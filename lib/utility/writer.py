# coding=utf-8
# 保存结果到文件

from lib.utility.path import *


def make_dir(dir_name):
    pass


def write_urls_to_file(file_name, urls):
    file_name = DATA_PATH + "/" + file_name
    txt_file = open(file_name, 'w')
    for url in urls:
        txt_file.write(url+"\n")
    txt_file.close()
