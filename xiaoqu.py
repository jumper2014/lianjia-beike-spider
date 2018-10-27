#!/usr/bin/env python
# coding=utf-8
# author: Zeng YueTian
# 此代码仅供学习与交流，请勿用于商业用途。
# 获得指定城市的小区数据
# 这些数据包括:
# 日期,所属区县,板块名,小区名,挂牌均价,挂牌数
# 20180221,浦东,川沙,恒纬家苑,32176元/m2,3套在售二手房

from lib.spider.xiaoqu_spider import *

if __name__ == "__main__":
    spider = XiaoQuBaseSpider(SPIDER_NAME)
    spider.start()
