#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 判断Python版本环境


import sys

if sys.version_info < (3, 0):   # 如果小于Python3
    PYTHON_3 = False
else:
    PYTHON_3 = True

if not PYTHON_3:   # 如果小于Python3
    reload(sys)
    sys.setdefaultencoding("utf-8")
