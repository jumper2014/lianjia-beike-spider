#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 获得各城市的区县相关信息

import requests
from lxml import etree
from lib.city.city import cities
from lib.const.xpath import *

chinese_city_district_dict = dict()     # 城市代码和中文名映射
chinese_area_dict = dict()              # 版块代码和中文名映射
area_dict = dict()


def get_chinese_district(en):
    """
    拼音区县名转中文区县名
    :param en: 拼音
    :return: 中文
    """
    return chinese_city_district_dict.get(en, None)


def get_districts(city):
    url = 'https://{0}.lianjia.com/xiaoqu/'.format(city)
    response = requests.get(url, timeout=10)
    html = response.content
    root = etree.HTML(html)
    elements = root.xpath(CITY_DISTRICT_XPATH)
    en_names = list()
    ch_names = list()
    for element in elements:
        link = element.attrib['href']
        en_names.append(link.split('/')[-2])
        ch_names.append(element.text)

        # 打印区县英文和中文名列表
    for index, name in enumerate(en_names):
        chinese_city_district_dict[name] = ch_names[index]
        # print(name + ' -> ' + ch_names[index])
    return en_names


if __name__ == '__main__':
    for key in cities.keys():
        # 寻找那些网页格式不合规的城市
        chinese_city_district_dict = dict()
        get_districts(key)
        if len(chinese_city_district_dict.items()) == 0:
            print(key)
