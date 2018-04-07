#!/usr/bin/env python
# coding=utf-8
# author: Zeng YueTian
# 获得指定城市的所有出租房数据


import math
from lib.utility.date import *
from lib.utility.path import *
from lib.url.xiaoqu import *
from lib.city.city import *
from lib.city.loupan import *
from lib.utility.version import PYTHON_3


def collect_city_loupan(city, fmt="csv"):
    """
    对于每个板块,获得这个板块下所有出租房的信息
    并且将这些信息写入文件保存
    :param city: 城市
    :param fmt: 保存文件格式
    :return: None
    """
    global total_num, today_path
    csv_file = today_path + "/{0}.csv".format(city)
    with open(csv_file, "w") as f:
        # 开始获得需要的板块数据
        loupans = get_loupan_info(city)
        total_num = len(loupans)
        if fmt == "csv":
            for loupan in loupans:
                f.write(date_string + "," + loupan.text() + "\n")
    print("Finish crawl: " + city + ", save data to : " + csv_file)


def get_loupan_info(city):
    loupan_list = list()
    page = 'http://{0}.fang.lianjia.com/loupan/'.format(city)
    print(page)

    response = requests.get(page, timeout=10)
    html = response.content
    soup = BeautifulSoup(html, "lxml")

    # 获得总的页数
    try:
        page_box = soup.find_all('div', class_='page-box')[0]
        matches = re.search('.*data-total-count="(\d+)".*', str(page_box))
        total_page = math.ceil(int(matches.group(1)) / 10)
    except Exception as e:
        print("\tWarning: only find one page for {0}".format(city))
        print("\t" + e.message)
        total_page = 1

    # 从第一页开始,一直遍历到最后一页
    for i in range(1, total_page + 1):
        page = 'http://{0}.fang.lianjia.com/loupan/pg{1}'.format(city, i)
        print(page)
        response = requests.get(page, timeout=10)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得有小区信息的panel
        house_elems = soup.find_all('li', class_="resblock-list")
        for house_elem in house_elems:
            price = house_elem.find('span', class_="number")
            total = house_elem.find('div', class_="second")
            xiaoqu = house_elem.find('a', class_='name')

            # 继续清理数据
            try:
                price = price.text.strip()
            except:
                price = '0'
            xiaoqu = xiaoqu.text.replace("\n", "")
            try:
                total = total.text.strip().replace(u'总价', '')
                total = total.replace(u'/套起', '')
            except:
                total = '0'

            print("{0} {1} {2} ".format(
                xiaoqu, price, total))

            # 作为对象保存
            loupan = LouPan(xiaoqu, price, total)
            loupan_list.append(loupan)
    return loupan_list


# -------------------------------
# main函数从这里开始
# -------------------------------
if __name__ == "__main__":
    # 让用户选择爬取哪个城市的出租房价格数据
    prompt = create_prompt_text()
    # 判断Python版本
    if not PYTHON_3:  # 如果小于Python3
        city = raw_input(prompt)
    else:
        city = input(prompt)
    print('OK, start to crawl ' + get_chinese_city(city))

    total_num = 0
    # 准备日期信息，爬到的数据存放到日期相关文件夹下
    date_string = get_date_string()
    print('Today date is: %s' % date_string)
    today_path = create_date_path("loupan", city, date_string)
    t1 = time.time()  # 开始计时

    collect_city_loupan(city)
    # 计时结束，统计结果
    t2 = time.time()
    print("Total crawl {0} loupan.".format(total_num))
    print("Total cost {0} second ".format(t2 - t1))
