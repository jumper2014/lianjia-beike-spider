# coding=utf-8

import requests
from BeautifulSoup import BeautifulSoup
from lxml import etree
import re

base_url = "http://sh.lianjia.com"

if __name__ == "__main__":
    second_hand_url = "http://sh.lianjia.com/ershoufang/"

    response = requests.get(second_hand_url)
    html = response.content

    # soup = BeautifulSoup(html)
    root = etree.HTML(html)
    print root

    xpath_str = '//*[@id="filter-options"]/dl[1]/dd/div/a'
    links = root.xpath(xpath_str)
    # print links
    for link in links:
        print base_url + link.attrib['href']




