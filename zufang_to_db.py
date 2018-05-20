#!/usr/bin/env python
# coding=utf-8
# author: Zeng YueTian
# 获得指定城市的出租房数据

import pymysql
import threadpool
import threading

from lib.utility.date import *
from lib.city.area import *
from lib.utility.path import *
from lib.url.xiaoqu import *
from lib.city.city import *
from lib.city.zufang import *
from lib.utility.version import PYTHON_3
from lib.const.spider import thread_pool_size

pymysql.install_as_MySQLdb()


def collect_area_zufang(city_name, area_name):
    """
    对于每个板块,获得这个板块下所有出租房的信息
    并且将这些信息写入文件保存
    :param city_name: 城市
    :param area_name: 板块
    :param fmt: 保存文件格式
    :return: None
    """
    global total_num, today_path

    # 开始获得需要的板块数据
    zufangs = get_area_zufang_info(city_name, area_name)

    for zufangItem in zufangs:
        # 锁定
        if mutex.acquire(1):
            total_num += len(zufangs)
            # 释放
            mutex.release()

        price = str(zufangItem.price).replace(r'暂无', '0')
        price = price.replace(r'元/m2', '')
        price = int(price)

        size = zufangItem.size.replace(r'平米', '')
        update_date = zufangItem.update_date

        print("{0} {1} {2} {3} {4} {5} {6}".format(update_date, district, zufangItem.area,
                                                   zufangItem.xiaoqu, price, zufangItem.layout,
                                                   size))

        # 写入mysql数据库
        try:
            if  mutex.acquire(1) and database == "mysql":
                db.query(
                    'INSERT INTO zufang ( update_date, district, area, xiaoqu, price, layout, size) '
                    'VALUES(:update_date, :district, :area, :xiaoqu, :price, :layout, :size)',
                    update_date=zufangItem.update_date, district=zufangItem.district,
                    area=zufangItem.area, xiaoqu=zufangItem.xiaoqu,  price=price,
                    layout=zufangItem.layout, size=size)

                mutex.release()
        except Exception as e:
            print("excetion~~~~~~~~~~~", e)
            mutex.release()

    print("Finish save to mysql,city={0},area={1}".format(city_name, area_name))


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
    page = 'http://{0}.lianjia.com/zufang/{1}/'.format(city_name, area_name)
    print(page)

    response = requests.get(page, timeout=10)
    html = response.content
    soup = BeautifulSoup(html, "lxml")

    # 获得总的页数
    try:
        page_box = soup.find_all('div', class_='page-box')[0]
        matches = re.search('.*"totalPage":(\d+),.*', str(page_box))
        total_page = int(matches.group(1))
    except Exception as e:
        print("\tWarning: only find one page for {0}".format(area_name))
        print("\t exception", e)
        total_page = 1

    # 从第一页开始,一直遍历到最后一页
    for num in range(1, total_page + 1):
        page = 'http://{0}.lianjia.com/zufang/{1}/pg{2}'.format(city_name, area_name, num)
        print(page)
        response = requests.get(page, timeout=10)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得有小区信息的panel
        ul_element = soup.find('ul', class_="house-lst")
        house_elements = ul_element.find_all('li')
        for house_elem in house_elements:
            price = house_elem.find('span', class_="num")
            xiaoqu = house_elem.find('span', class_='region')
            layout = house_elem.find('span', class_="zone")
            size = house_elem.find('span', class_="meters")
            updateDate = house_elem.find('div', class_="price-pre")

            # 继续清理数据
            if price is None:
                price = -1
            else:
                price = price.text.strip()

            if xiaoqu is None:
                xiaoqu = '未知'
            else:
                xiaoqu = xiaoqu.text.strip().replace("\n", "")

            if layout is None:
                layout = '未知'
            else:
                layout = layout.text.strip()

            if size is None:
                size = '-1'
            else:
                size = size.text.strip()

            if updateDate is None:
                updateDate = '未知'
            else:
                updateDate = updateDate.text.strip().replace(".", "").replace(" ", "").replace("更新", "")

            # print("{0} {1} {2} {3} {4} {5} {6}".format(
            #     chinese_district, chinese_area, xiaoqu, layout, size, price))

            # 作为对象保存
            zufang = ZuFang(chinese_district, chinese_area, xiaoqu, layout, size, price, updateDate)
            zufang_list.append(zufang)
    return zufang_list


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

    # 准备日期信息，爬到的数据存放到日期相关文件夹下
    date_string = get_date_string()
    print('Today date is: %s' % date_string)
    today_path = create_date_path("zufang", city, date_string)

    # collect_area_zufang('sh', 'beicai')  # For debugging, keep it here

    database = "mysql"
    db = None
    if database == "mysql":
        import records
        db = records.Database('mysql://root:123456@localhost/lianjia?charset=utf8',
                              encoding='utf-8')
        # 清空数据库历史旧数据
        db.query('delete from zufang')
    # TODO 加入mongodb的支持

    mutex = threading.Lock()  # 创建锁
    total_num = 0  # 总的小区个数，用于统计
    t1 = time.time()  # 开始计时

    # 获得城市有多少区列表, district: 区县
    districts = get_districts(city)
    print('City: {0}'.format(city))
    print('Districts: {0}'.format(districts))

    # 获得每个区的板块, area: 板块
    areas = list()
    for district in districts:
        areas_of_district = get_areas(city, district)
        print('{0}: Area list:  {1}'.format(district, areas_of_district))
        # 用list的extend方法,L1.extend(L2)，该方法将参数L2的全部元素添加到L1的尾部
        areas.extend(areas_of_district)
        # 使用一个字典来存储区县和板块的对应关系, 例如{'beicai': 'pudongxinqu', }
        for area in areas_of_district:
            area_dict[area] = district
    print("Area:", areas)
    print("District and areas:", area_dict)

    # 准备线程池用到的参数
    nones = [None for i in range(len(areas))]
    city_list = [city for i in range(len(areas))]
    args = zip(zip(city_list, areas), nones)
    # areas = areas[0: 1]

    # 针对每个板块写一个文件,启动一个线程来操作
    pool_size = thread_pool_size
    pool = threadpool.ThreadPool(pool_size)
    my_requests = threadpool.makeRequests(collect_area_zufang, args)
    [pool.putRequest(req) for req in my_requests]
    pool.wait()
    pool.dismissWorkers(pool_size, do_join=True)  # 完成后退出

    # 计时结束，统计结果
    t2 = time.time()
    print("Total crawl {0} areas.".format(len(areas)))
    print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, total_num))
