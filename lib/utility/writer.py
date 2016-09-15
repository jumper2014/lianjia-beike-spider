# coding=utf-8
#

from lib.const.path import *


def write_urls_to_file(file_name, urls):
    file_name = DATA_PATH + "/" + file_name
    txt_file = open(file_name, 'w')
    for url in urls:
        txt_file.write(url+"\n")
    txt_file.close()
