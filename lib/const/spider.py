#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian

from lib.city.city import lianjia_cities, beike_cities
import sys
from lib.utility.version import PYTHON_3
from lib.utility.log import *

thread_pool_size = 50
LIANJIA_SPIDER = "lianjia"
BEIKE_SPIDER = "ke"
SPIDER_NAME = LIANJIA_SPIDER
# SPIDER_NAME = BEIKE_SPIDER


class Spider(object):
    def __init__(self, name):
        self.name = name
        if self.name == LIANJIA_SPIDER:
            self.cities = lianjia_cities
        elif self.name == BEIKE_SPIDER:
            self.cities = beike_cities
        else:
            self.cities = None

    def create_prompt_text(self):
        """
        根据已有城市中英文对照表拼接选择提示信息
        :return: 拼接好的字串
        """
        city_info = list()
        count = 0
        for en_name, ch_name in self.cities.items():
            count += 1
            city_info.append(en_name)
            city_info.append(": ")
            city_info.append(ch_name)
            if count % 4 == 0:
                city_info.append("\n")
            else:
                city_info.append(", ")
        return 'Which city do you want to crawl?\n' + ''.join(city_info)

    def get_chinese_city(self, en):
        """
        拼音拼音名转中文城市名
        :param en: 拼音
        :return: 中文
        """
        return self.cities.get(en, None)

    def get_city(self):

        # 允许用户通过命令直接指定
        if len(sys.argv) < 2:
            print("Wait for your choice.")
            # 让用户选择爬取哪个城市的二手房小区价格数据
            prompt = self.create_prompt_text()
            # 判断Python版本
            if not PYTHON_3:  # 如果小于Python3
                city = raw_input(prompt)
            else:
                city = input(prompt)
        elif len(sys.argv) == 2:
            city = str(sys.argv[1])
            print("City is: {0}".format(city))
        else:
            print("At most accept one parameter.")
            exit(1)

        chinese_city = self.get_chinese_city(city)
        if chinese_city is not None:
            message = 'OK, start to crawl ' + self.get_chinese_city(city)
            print(message)
            logger.info(message)
        else:
            print("No such city, please check your input.")
            exit(1)
        return city


