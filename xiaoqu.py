# coding=utf-8
# author: Zeng YueTian
# 获得指定城市的所有小区数据
# 这些数据包括:
# 日期,所属区县,板块名,小区名,挂牌均价,挂牌数
# 20180221,浦东,川沙,恒纬家苑,32176元/m2,3套在售二手房

import threadpool
import threading
from lib.utility.date import *
from lib.city.area import *
from lib.utility.path import *
from lib.url.xiaoqu import *


def collect_xiaoqu_data(area_name, fmt="csv"):
    """
    对于每个板块,获得这个板块下所有小区的信息
    并且将这些信息写入文件保存
    :param area_name: 板块
    :param fmt: 保存文件格式
    :return: None
    """
    global total_num, today_path

    csv_file = today_path + "/{0}.csv".format(area_name)
    with open(csv_file, "w") as f:
        # 开始获得需要的板块数据
        xiaoqus = get_xiaoqu_info("sh", area_name)
        # 锁定
        if mutex.acquire(1):
            total_num += len(xiaoqus)
            # 释放
            mutex.release()
        if fmt == "csv":
            for xiaoqu in xiaoqus:
                # print(date_string + "," + xiaoqu.text())
                f.write(date_string + "," + xiaoqu.text()+"\n")
    print("Finish crawl area: " + area_name + ", save data to : " + csv_file)


# -------------------------------
# main函数从这里开始
# -------------------------------
if __name__ == "__main__":
    city = "sh"
    date_string = get_date_string()
    print('Today date is: %s' % date_string)
    today_path = create_date_path("lianjia", city, date_string)

    # 创建锁
    mutex = threading.Lock()

    # 总的小区个数
    total_num = 0

    # 开始计时
    t1 = time.time()

    # -------------------------------
    # 获得上海有多少区列表, district: 区县
    # -------------------------------
    districts = get_districts(city)
    print('City: {0}'.format(city))
    print('Districts: {0}'.format(districts))

    # -------------------------------
    # 获得每个区的板块, area: 板块
    # -------------------------------
    areas = list()
    for district in districts:
        areas_of_district = get_areas("sh", district)
        print('{0}: Area list:  {1}'.format(district, areas_of_district))
        # 用list的extend方法,L1.extend(L2)，该方法将参数L2的全部元素添加到L1的尾部
        areas.extend(areas_of_district)
        # 使用一个字典来存储区县和板块的对应关系, 例如{'beicai': 'pudongxinqu', }
        for area in areas_of_district:
            AREA_DICT[area] = district

    print("Area:", areas)
    print("District and areas:", AREA_DICT)

    # areas = areas[0: 1]
    # 针对每个板块写一个文件,启动一个线程来操作
    # 使用线程池来做
    pool_size = 50
    pool = threadpool.ThreadPool(pool_size)

    requests = threadpool.makeRequests(collect_xiaoqu_data, areas)

    [pool.putRequest(req) for req in requests]
    pool.poll()
    pool.wait()

    # 完成后退出
    pool.dismissWorkers(pool_size, do_join=True)

    # 计时结束
    t2 = time.time()
    print("Total crawl {0} areas.".format(len(areas)))
    print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, total_num))
