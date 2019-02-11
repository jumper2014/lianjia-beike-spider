#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 获取城市挂牌二手房数量

import time
from lib.spider.base_spider import SPIDER_NAME
from bs4 import BeautifulSoup
from lib.zone.city import cities
import requests

numbers = dict()


def get_ershou_number(city):
    url = "https://{0}.{1}.com/ershoufang/".format(city, SPIDER_NAME)
    print(url)
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "lxml")
    element = soup.find('h2', class_='total')
    number = int(element.text.split(" ")[1].strip())
    numbers[city] = number


if __name__ == '__main__':
    start = time.time()
    for key, value in cities.items():
        # print(key, value)
        get_ershou_number(key)
    for k, v in numbers.items():
        print(cities[k], v)
    print("cost {0} seconds".format(time.time() - start))
