# coding=utf-8
#

import requests
from lxml import etree
from lib.const.url import *


def get_urls_from_xpath(page, xpath, relative=True):
    response = requests.get(page)
    html = response.content
    root = etree.HTML(html)
    links = root.xpath(xpath)
    if relative:
        return [BASE_URL + link.attrib['href'] for link in links]
    else:
        return [link.attrib['href'] for link in links]
