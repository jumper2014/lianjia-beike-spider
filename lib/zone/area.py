#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 板块信息相关函数

from lib.zone.district import *
from lib.const.xpath import *
from lib.request.headers import *
from lib.spider.base_spider import SPIDER_NAME
import sys
from lib.utility.version import PYTHON_3
from lib.utility.log import *


def get_district_url(city, district):
    """
    拼接指定城市的区县url
    :param city: 城市
    :param district: 区县
    :return:
    """
    return "http://{0}.{1}.com/xiaoqu/{2}".format(city, SPIDER_NAME, district)

def create_prompt_text():
    return '请选择你要爬取的区域,多个之间用逗号分隔(例如:dongcheng,xicheng),如果不限制，则输入all \n'

def get_selectareas():
     districts = None
    # 允许用户通过命令直接指定
     if len(sys.argv) < 2:
        # 让用户选择爬取哪个城市的二手房小区价格数据
        prompt = create_prompt_text()
        # 判断Python版本
        if not PYTHON_3:  # 如果小于Python3
            districts = raw_input(prompt)
        else:
            districts = input(prompt)
     elif len(sys.argv) == 2:
        districts = str(sys.argv[1])
        print("区域 is: {0}".format(districts))
     else:
        print("At most accept one parameter.")
        exit(1)
     return districts.split(',')

def get_areas(city, district):
    """
    通过城市和区县名获得下级板块名
    :param city: 城市
    :param district: 区县
    :return: 区县列表
    """
    page = get_district_url(city, district)
    areas = list()
    try:
        headers = create_headers()
        response = requests.get(page, timeout=10, headers=headers)
        html = response.content
        root = etree.HTML(html)
        links = root.xpath(DISTRICT_AREA_XPATH)

        # 针对a标签的list进行处理
        for link in links:
            relative_link = link.attrib['href']
            # 去掉最后的"/"
            relative_link = relative_link[:-1]
            # 获取最后一节
            area = relative_link.split("/")[-1]
            # 去掉区县名,防止重复
            if area != district:
                chinese_area = link.text
                chinese_area_dict[area] = chinese_area
                # print(chinese_area)
                areas.append(area)
        return areas
    except Exception as e:
        print(e)


if __name__ == "__main__":
    print(get_areas("sh", "huangpu"))

