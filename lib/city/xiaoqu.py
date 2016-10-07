# coding=utf-8
# author: Zeng YueTian
# 小区信息的数据结构
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class XiaoQu(object):
    def __init__(self, price, name, on_sale):
        self.price = price
        self.name = name
        self.on_sale = on_sale

    def text(self):
        return self.name+","+self.price+","+self.on_sale
