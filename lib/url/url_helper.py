#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian

import urllib2
from lxml import etree
from lib.const.url import *


def get_urls_from_xpath(page, xpath, relative=True):
    try:
        response = urllib2.urlopen(page)
        html = response.read()
        root = etree.HTML(html)
        links = root.xpath(xpath)
        if relative:
            for link in links:
                # print link.text
                pass
            return [LIANJIA_SH_BASE_URL + link.attrib['href'] for link in links]
        else:
            return [link.attrib['href'] for link in links]
    except Exception as e:
        print e
