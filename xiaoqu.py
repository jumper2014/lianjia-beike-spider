# coding=utf-8
# author: Zeng YueTian
# 获得城市小区数据

import time
import threadpool
from lib.city.district import *
from lib.city.area import *
from lib.utility.path import *
from lib.url.xiaoqu import *


def collect_xiaoqu_data(area):
    """
    对于每个板块,获得这个板块下所有小区的信息
    并且将这些信息写入文件保存
    :param area: 板块
    :return: None
    """
    print "Collect and archive ", area
    csv_file = get_root_path() + "/data/{0}.csv".format(area)
    with open(csv_file, "w") as f:
        # 开始获得需要的板块数据
        xiaoqu_list = get_xiaoqu_info("sh", area)
        for xiaoqu in xiaoqu_list:
            # text = str(xiaoqu)
            f.write(xiaoqu.text()+"\n")


# -------------------------------
# main函数从这里开始
# -------------------------------
if __name__ == "__main__":
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
    areas = []
    area_dict = dict()
    for district in districts:
        areas_of_district = get_areas("sh", district)
        # 用list的extend方法,L1.extend(L2)，该方法将参数L2的全部元素添加到L1的尾部
        areas.extend(areas_of_district)
        # 使用一个字典来存储区县和板块的对应关系, 例如{'beicai': 'pudongxinqu', }
        for area in areas_of_district:
            area_dict[area] = district

    print "板块:", areas
    print "区县和板块对应关系", area_dict

    areas = areas[0: 1]
    # 针对每个板块写一个文件,启动一个线程来操作
    # 使用线程池来做
    pool_size = 10
    pool = threadpool.ThreadPool(pool_size)

    requests = threadpool.makeRequests(collect_xiaoqu_data, areas)

    [pool.putRequest(req) for req in requests]
    pool.poll()
    pool.wait()

    # 完成后退出
    pool.dismissWorkers(pool_size, do_join=True)

    t2 = time.time()
    print "Cost {0} seconds to finish".format(t2 - t1)












