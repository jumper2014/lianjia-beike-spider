# coding=utf-8
# author: yuetian

import requests
from lxml import etree
from lib.const.url import *
from lib.const.xpath import *
from lib.url.url_helper import *


def get_qu_urls():
    return get_urls_from_xpath(ERSHOUFANG_BASE_URL, ERSHOUFANG_QU_XPATH)


def get_sub_qu_urls():
    urls = []
    for link in get_qu_urls():
        for sub_link in get_urls_from_xpath(link, ERSHOUFANG_SUB_QU_XPATH):
            urls.append(sub_link)
    return urls


