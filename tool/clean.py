#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 清理结果文件

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