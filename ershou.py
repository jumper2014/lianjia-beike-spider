# coding=utf-8
# author: Zeng YueTian
# 获得指定城市的所有二手房数据


import threadpool
import threading
from lib.utility.date import *
from lib.city.area import *
from lib.utility.path import *
from lib.url.xiaoqu import *
from lib.city.city import *
from lib.city.ershou import *


def collect_xiaoqu_data(city, area_name, fmt="csv"):
    """
    对于每个板块,获得这个板块下所有小区的信息
    并且将这些信息写入文件保存
    :param city: 城市
    :param area_name: 板块
    :param fmt: 保存文件格式
    :return: None
    """
    global total_num, today_path

    csv_file = today_path + "/{0}.csv".format(area_name)
    with open(csv_file, "w") as f:
        # 开始获得需要的板块数据
        xqs = get_xiaoqu_info(city, area_name)
        # 锁定
        if mutex.acquire(1):
            total_num += len(xqs)
            # 释放
            mutex.release()
        if fmt == "csv":
            for xiaoqu in xqs:
                # print(date_string + "," + xiaoqu.text())
                f.write(date_string + "," + xiaoqu.text()+"\n")
    print("Finish crawl area: " + area_name + ", save data to : " + csv_file)


def collect_area_ershou(city, area_name, fmt="csv"):
    """
    对于每个板块,获得这个板块下所有二手房的信息
    并且将这些信息写入文件保存
    :param city: 城市
    :param area_name: 板块
    :param fmt: 保存文件格式
    :return: None
    """
    global total_num, today_path

    csv_file = today_path + "/{0}.csv".format(area_name)
    with open(csv_file, "w") as f:
        # 开始获得需要的板块数据
        ershous = get_area_ershou_info(city, area_name)
        # 锁定
        if mutex.acquire(1):
            total_num += len(ershous)
            # 释放
            mutex.release()
        if fmt == "csv":
            for ershou in ershous:
                # print(date_string + "," + xiaoqu.text())
                f.write(date_string + "," + ershou.text()+"\n")
    print("Finish crawl area: " + area_name + ", save data to : " + csv_file)


def get_area_ershou_info(city, area):
    district = area_dict.get(area, "")
    chinese_district = get_chinese_district(district)
    chinese_area = chinese_area_dict.get(area, "")
    ershou_list = list()
    page = 'http://{0}.lianjia.com/ershoufang/{1}/'.format(city, area)
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
        print("\tWarning: only find one page for {0}".format(area))
        print("\t" + e.message)
        total_page = 1

    # 从第一页开始,一直遍历到最后一页
    for i in range(1, total_page + 1):
        page = 'http://{0}.lianjia.com/ershoufang/{1}/pg{2}'.format(city, area, i)
        print(page)
        response = requests.get(page, timeout=10)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得有小区信息的panel
        house_elems = soup.find_all('li', class_="clear")
        for house_elem in house_elems:
            price = house_elem.find('div', class_="totalPrice")
            name = house_elem.find('div', class_='title')
            desc = house_elem.find('div', class_="houseInfo")

            # 继续清理数据
            price = price.text.strip()
            name = name.text.replace("\n", "")
            desc = desc.text.replace("\n", "").strip()

            # 作为对象保存
            ershou = ErShou(chinese_district, chinese_area, name, price, desc)
            ershou_list.append(ershou)
    return ershou_list


def create_prompt_text():
    city_info = list()
    count = 0
    for en_name, ch_name in cities.items():
        count += 1
        city_info.append(en_name)
        city_info.append(": ")
        city_info.append(ch_name)
        if count % 4 == 0:
            city_info.append("\n")
        else:
            city_info.append(", ")
    return 'Which city do you want to crawl?\n' + ''.join(city_info)


# -------------------------------
# main函数从这里开始
# -------------------------------
if __name__ == "__main__":
    # 让用户选择爬取哪个城市的二手房小区价格数据
    prompt = create_prompt_text()
    # 判断Python版本
    import sys
    if sys.version_info < (3, 0):   # 如果小于Python3
        city = raw_input(prompt)
    else:
        city = input(prompt)

    print('OK, start to crawl ' + get_chinese_city(city))

    # 准备日期信息，爬到的数据存放到日期相关文件夹下
    date_string = get_date_string()
    print('Today date is: %s' % date_string)
    today_path = create_date_path("ershou", city, date_string)

    mutex = threading.Lock()    # 创建锁
    total_num = 0               # 总的小区个数，用于统计
    t1 = time.time()            # 开始计时

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
    pool_size = 50
    pool = threadpool.ThreadPool(pool_size)
    my_requests = threadpool.makeRequests(collect_area_ershou, args)
    [pool.putRequest(req) for req in my_requests]
    pool.wait()
    pool.dismissWorkers(pool_size, do_join=True)        # 完成后退出

    # 计时结束，统计结果
    t2 = time.time()
    print("Total crawl {0} areas.".format(len(areas)))
    print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, total_num))
