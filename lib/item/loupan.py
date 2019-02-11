#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 新房楼盘的数据结构


class LouPan(object):
    def __init__(self, xiaoqu, price, total):
        # self.district = district
        # self.area = area
        self.xiaoqu = xiaoqu
        # self.address = address
        # self.size = size
        self.price = price
        self.total = total

    def text(self):
        return self.xiaoqu + "," + \
                self.price + "," + \
                self.total
