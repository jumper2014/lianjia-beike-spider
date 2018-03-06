# coding=utf-8
# author: Zeng YueTian
# 各城市的区县相关信息

CHINESE_DISTRICT_DICT = {
    "pudong": "浦东",
    "minhang": "闵行",
    "baoshan": "宝山",
    "xuhui": "徐汇",
    "putuo": "普陀",
    "yangpu": "杨浦",
    "changning": "长宁",
    "songjiang": "松江",
    "jiading": "嘉定",
    "huangpu": "黄浦",
    "jingan": "静安",
    "zhabei": "闸北",
    "hongkou": "虹口",
    "qingpu": "青浦",
    "fengxian": "奉贤",
    "jinshan": "金山",
    "chongming": "崇明",

    'dongcheng': '东城',
    'xicheng': '西城',
    'chaoyang': '朝阳',
    'haidian': '海淀',
    'fengtai': '丰台',
    'shijingshan': '石景山',
    'tongzhou': '通州',
    'changping': '昌平',
    'daxing': '大兴',
    'yizhuangkaifaqu': '亦庄开发区',
    'shunyi': '顺义',
    'fangshan': '房山',
    'mentougou': '门头沟',
    'pinggu': '平谷',
    'huairou': '怀柔',
    'miyun': '密云',
    'yanqing': '延庆',
    'yanjiao': '燕郊',
}

CHINESE_AREA_DICT = dict()

SHANGHAI_DISTRICT_LIST = [
    "pudong",
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
    'dongcheng',
    'xicheng',
    'chaoyang',
    'haidian',
    'fengtai',
    'shijingshan',
    'tongzhou',
    'changping',
    'daxing',
    'yizhuangkaifaqu',
    'shunyi',
    'fangshan',
    'mentougou',
    'pinggu',
    'huairou',
    'miyun',
    'yanqing',
    'yanjiao',

]

AREA_DICT = dict()


def get_chinese_district(en):
    """
    拼音区县名转中文区县名
    :param en: 拼音
    :return: 中文
    """
    return CHINESE_DISTRICT_DICT.get(en, None)


def get_districts(city):
    if city in ("sh"):
        return SHANGHAI_DISTRICT_LIST
    elif city in ("bj"):
        return BEIJING_DISTRICT_LIST
