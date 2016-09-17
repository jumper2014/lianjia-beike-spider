# coding=utf-8
# 文件和目录以时间戳命名

import time


def get_time_string():
    current = time.localtime()
    return time.strftime("%Y%m%d%H%M%S", current)


def get_date_string():
    current = time.localtime()
    return time.strftime("%Y%m%d", current)


if __name__ == "__main__":
    print get_date_string()