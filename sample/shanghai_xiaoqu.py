# coding=utf-8
# 获得链家上各个小区的挂牌均价
# 包括:小区名,所属区,所属板块,挂牌均价,建造时间,距离地铁,在售二手房套数

from lib.utility.date import *
from lib.utility.path import *
from lib.city.district import *

if __name__ == "__main__":
    # create dir for data/lianjia/city/date
    date_string = get_date_string()
    today_path = create_date_path("lianjia", "shanghai", date_string)

    # find the 市区(disctrict)
    district_list = get_city_districts("shanghai")

    for district in district_list:
        print district



    # find the 板块(area)
    # create dir for each bankuai

    # for each bankuai

    # find total pages

    # for each page

    # find xiaoqu's data

    # save xiaoqu's data to csv file

    pass

