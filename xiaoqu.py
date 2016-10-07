# coding=utf-8
# author: Zeng YueTian
# 获得指定城市的小区数据

import time
import threadpool
import threading
from lib.city.area import *
from lib.utility.path import *
from lib.url.xiaoqu import *


def collect_xiaoqu_data(area_name):
    """
    对于每个板块,获得这个板块下所有小区的信息
    并且将这些信息写入文件保存
    :param area_name: 板块
    :return: None
    """
    global total_num
    csv_file = get_root_path() + "/data/{0}.csv".format(area_name)
    print "开始爬取板块:", area_name, "保存文件路径:", csv_file
    with open(csv_file, "w") as f:
        # 开始获得需要的板块数据
        xiaoqu_list = get_xiaoqu_info("sh", area_name)
        # 锁定
        if mutex.acquire(1):
            total_num += len(xiaoqu_list)
            # 释放
            mutex.release()
        for xiaoqu in xiaoqu_list:
            f.write(xiaoqu.text()+"\n")
    print "完成爬取板块:", area_name


# -------------------------------
# main函数从这里开始
# -------------------------------
if __name__ == "__main__":
    # 创建锁
    mutex = threading.Lock()

    # 总的小区个数
    total_num = 0

    # 开始计时
    t1 = time.time()

    # -------------------------------
    # 获得上海有多少区列表, district: 区县
    # -------------------------------
    districts = get_districts("sh")
    print "区县:", districts

    # -------------------------------
    # 获得每个区的板块, area: 板块
    # -------------------------------
    areas = list()
    for district in districts:
        areas_of_district = get_areas("sh", district)
        # 用list的extend方法,L1.extend(L2)，该方法将参数L2的全部元素添加到L1的尾部
        areas.extend(areas_of_district)
        # 使用一个字典来存储区县和板块的对应关系, 例如{'beicai': 'pudongxinqu', }
        for area in areas_of_district:
            AREA_DICT[area] = district

    print "板块:", areas
    print "区县和板块对应关系:", AREA_DICT

    # areas = areas[0: 1]
    # 针对每个板块写一个文件,启动一个线程来操作
    # 使用线程池来做
    pool_size = 5
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












