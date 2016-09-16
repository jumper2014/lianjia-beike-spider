# coding=utf-8
# author: yuetian

import requests
from lxml import etree
from lib.const.url import *
from lib.const.xpath import *
from lib.url.url_helper import *


def get_xiaoqu_qu_urls():
    """
    获取小区栏目下面的各区导航链接
    :return:
    """
    urls = get_urls_from_xpath(SH_XIAOQU_BASE_URL, XIAOQU_QU_XPATH)
    print urls
    return urls


def get_xiaoqu_bankuai_urls():
    """
    获取小区栏目下面的各区下级板块导航链接
    :return:
    """
    urls = []
    for link in get_xiaoqu_qu_urls():
        for sub_link in get_urls_from_xpath(link, XIAOQU_BANKUAI_XPATH):
            urls.append(sub_link)
    return urls


if __name__ == "__main__":
    urls = get_xiaoqu_bankuai_urls()
    print urls


