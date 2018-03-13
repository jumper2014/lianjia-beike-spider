#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian

from lib.const.xpath import *
from lib.url.url_helper import *


def get_ershoufang_qu_urls():
    """
    获得二手房栏目下面的各区导航链接
    :return:
    """
    return get_urls_from_xpath(ERSHOUFANG_BASE_URL, ERSHOUFANG_QU_XPATH)


def get_ershoufang_bankuai_urls():
    """
    获得二手房栏目下面的各区下级板块导航链接
    :return:
    """
    urls = []
    for link in get_ershoufang_qu_urls():
        for sub_link in get_urls_from_xpath(link, ERSHOUFANG_BANKUAI_XPATH):
            if sub_link not in urls:
                urls.append(sub_link)
    return urls


