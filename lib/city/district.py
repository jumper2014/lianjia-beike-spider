# coding=utf-8
# author: Zeng YueTian
# 各城市的区县相关信息

SHANGHAI_DISTRICT_LIST = [
    "pudongxinqu",
    "minhang",
    "baoshan",
    "xuhui",
    "putuo",
    "yangpu",
    "changning",
    "songjiang",
    "jiading",
    "huangpu",
    "jingan",
    "zhabei",
    "hongkou",
    "qingpu",
    "fengxian",
    "jinshan",
    "chongming"
]

BEIJING_DISTRICT_LIST = [

]


def get_districts(city):
    if city == "shanghai" or "sh":
        return SHANGHAI_DISTRICT_LIST
    if city == "beijing" or "bej":
        return BEIJING_DISTRICT_LIST
