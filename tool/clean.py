#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian

from lib.utility.path import *

if __name__ == '__main__':
    # 删除日志
    os.system("rm -rf {0}/*.txt".format(LOG_PATH))

    # 删除爬取的数据
    os.system("rm -rf {0}/*".format(DATA_PATH))

    # 删除HTML
    os.system("rm -rf {0}/*.html".format(ROOT_PATH))

    # 删除csv
    os.system("rm -rf {0}/*.csv".format(ROOT_PATH))

    # 删除json
    os.system("rm -rf {0}/*.json".format(ROOT_PATH))