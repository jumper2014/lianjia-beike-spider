# coding=utf-8
#

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


def get_city_districts(city):
    if city == "shanghai" or "sh":
        return SHANGHAI_DISTRICT_LIST
