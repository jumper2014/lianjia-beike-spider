#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian

import requests
import threadpool
import threading
from lib.utility.date import *
from lib.zone.area import *
from lib.utility.path import *
from lib.url.xiaoqu import *
from lib.zone.city import *
from lib.item.zufang import *
from lib.utility.version import PYTHON_3
from lib.const.spider import *


def get_area_zufang_info(city_name, area_name):
    """
    通过爬取页面获取城市指定版块的租房信息
    :param city_name: 城市
    :param area_name: 版块
    :return: 出租房信息列表
    """
    district_name = area_dict.get(area_name, "")
    chinese_district = get_chinese_district(district_name)
    chinese_area = chinese_area_dict.get(area_name, "")
    zufang_list = list()
    page = 'http://{0}.{1}.com/zufang/{2}/'.format(city_name, SPIDER_NAME, area_name)
    print(page)

    headers = create_headers()
    response = requests.get(page, timeout=10, headers=headers)
    html = response.content
    soup = BeautifulSoup(html, "lxml")

    # 获得总的页数
    try:
        if SPIDER_NAME == "lianjia":
            page_box = soup.find_all('div', class_='page-box')[0]
            matches = re.search('.*"totalPage":(\d+),.*', str(page_box))
        elif SPIDER_NAME == "ke":
            page_box = soup.find_all('div', class_='content__pg')[0]
            # print(page_box)
            matches = re.search('.*data-totalpage="(\d+)".*', str(page_box))
        total_page = int(matches.group(1))
        # print(total_page)
    except Exception as e:
        print("\tWarning: only find one page for {0}".format(area_name))
        print(e)
        total_page = 1

    # 从第一页开始,一直遍历到最后一页
    headers = create_headers()
    for num in range(1, total_page + 1):
        page = 'http://{0}.{1}.com/zufang/{2}/pg{3}'.format(city_name, SPIDER_NAME, area_name, num)
        print(page)
        response = requests.get(page, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得有小区信息的panel
        if SPIDER_NAME == "lianjia":
            ul_element = soup.find('ul', class_="house-lst")
            house_elements = ul_element.find_all('li')
        else:
            ul_element = soup.find('div', class_="content__list")
            house_elements = ul_element.find_all('div', class_="content__list--item")

        if len(house_elements) == 0:
            continue
        # else:
        #     print(len(house_elements))

        for house_elem in house_elements:
            if SPIDER_NAME == "lianjia":
                price = house_elem.find('span', class_="num")
                xiaoqu = house_elem.find('span', class_='region')
                layout = house_elem.find('span', class_="zone")
                size = house_elem.find('span', class_="meters")
            else:
                price = house_elem.find('span', class_="content__list--item-price")
                desc1 = house_elem.find('p', class_="content__list--item--title")
                desc2 = house_elem.find('p', class_="content__list--item--des")

            try:
                if SPIDER_NAME == "lianjia":
                    price = price.text.strip()
                    xiaoqu = xiaoqu.text.strip().replace("\n", "")
                    layout = layout.text.strip()
                    size = size.text.strip()
                else:
                    # 继续清理数据
                    price = price.text.strip().replace(" ", "").replace("元/月","")
                    # print(price)
                    desc1 = desc1.text.strip().replace("\n", "")
                    desc2 = desc2.text.strip().replace("\n", "").replace(" ", "")
                    # print(desc1)

                    infos = desc1.split(' ')
                    xiaoqu = infos[0]
                    layout = infos[1]
                    descs = desc2.split('/')
                    # print(descs[1])
                    size = descs[1].replace("㎡", "平米")


                # print("{0} {1} {2} {3} {4} {5} {6}".format(
                #     chinese_district, chinese_area, xiaoqu, layout, size, price))

                # 作为对象保存
                zufang = ZuFang(chinese_district, chinese_area, xiaoqu, layout, size, price)
                zufang_list.append(zufang)
            except Exception as e:
                print("="*20 + " page no data")
                print(e)
                print(page)
                print("=" * 20)
    return zufang_list


if __name__ == '__main__':
    get_area_zufang_info("yt", "muping")