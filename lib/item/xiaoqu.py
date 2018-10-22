#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 小区信息的数据结构


import sys
if sys.version_info < (3, 0):   # 如果小于Python3
    reload(sys)
    sys.setdefaultencoding("utf-8")


class XiaoQu(object):
    def __init__(self, district, area, name, price, on_sale):
        self.district = district
        self.area = area
        self.price = price
        self.name = name
        self.on_sale = on_sale

    def text(self):
        return self.district + "," + \
                self.area + "," + \
                self.name + "," + \
                self.price + "," + \
                self.on_sale
