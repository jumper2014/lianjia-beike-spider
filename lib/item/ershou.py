#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 二手房信息的数据结构


class ErShou(object):
    def __init__(self, district, area, name, price, desc, pic):
        self.district = district
        self.area = area
        self.price = price
        self.name = name
        self.desc = desc
        self.pic = pic

    def text(self):
        return self.district + "," + \
                self.area + "," + \
                self.name + "," + \
                self.price + "," + \
                self.desc + "," + \
                self.pic
