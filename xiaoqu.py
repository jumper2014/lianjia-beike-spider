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


def collect_xiaoqu_data(area_name, dest="csv"):
    """
    对于每个板块,获得这个板块下所有小区的信息
    并且将这些信息写入文件保存
    :param area_name: 板块
    :return: None
    """
    global total_num, today_path

    csv_file = today_path + "/{0}.csv".format(area_name)
    print "开始爬取板块:", area_name, "保存文件路径:", csv_file
    with open(csv_file, "w") as f:
        # 开始获得需要的板块数据
        xiaoqus = get_xiaoqu_info("sh", area_name)
        # 锁定
        if mutex.acquire(1):
            total_num += len(xiaoqus)
            # 释放
            mutex.release()
        if dest == "csv":
            for xiaoqu in xiaoqus:
                # print(date_string + "," + xiaoqu.text())
                f.write(date_string + "," + xiaoqu.text()+"\n")
    print "完成爬取板块:", area_name


# -------------------------------
# main函数从这里开始
# -------------------------------
if __name__ == "__main__":

    date_string = get_date_string()
    print('Today date is: %s' % date_string)
    today_path = create_date_path("lianjia", "sh", date_string)

    # 创建锁
    mutex = threading.Lock()

    # 总的小区个数
    total_num = 0

    # 开始计时
    t1 = time.time()

    # -------------------------------
    # 获得上海有多少区列表, district: 区县
    # -------------------------------
    districts = get_districts("sh")   # 现在是hard coding
    print(u'区县: %s' % districts)

    # -------------------------------
    # 获得每个区的板块, area: 板块
    # -------------------------------
    print(u'开始抓取版块信息')
    areas = list()
    for district in districts:
        print(u'开始抓取区 %s' %district)

        areas_of_district = get_areas("sh", district)
        print(u'本区版块 %s' % areas_of_district)
        # 用list的extend方法,L1.extend(L2)，该方法将参数L2的全部元素添加到L1的尾部
        areas.extend(areas_of_district)
        # 使用一个字典来存储区县和板块的对应关系, 例如{'beicai': 'pudongxinqu', }
        for area in areas_of_district:
            AREA_DICT[area] = district

    print(u"板块:", areas)
    print(u"区县和板块对应关系:", AREA_DICT)

    # areas = areas[0: 1]
    # 针对每个板块写一个文件,启动一个线程来操作
    # 使用线程池来做
    pool_size = 20
    pool = threadpool.ThreadPool(pool_size)

    requests = threadpool.makeRequests(collect_xiaoqu_data, areas)

    [pool.putRequest(req) for req in requests]
    pool.poll()
    pool.wait()

    # 完成后退出
    pool.dismissWorkers(pool_size, do_join=True)

    # 计时结束
    t2 = time.time()
    print "一共 {0} 个小区.".format(len(areas))
    print "花费了 {0} 秒完成了 {1} 条数据的爬取.".format(t2 - t1, total_num)
