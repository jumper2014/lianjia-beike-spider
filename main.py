# coding=utf-8

import requests
from BeautifulSoup import BeautifulSoup
from lxml import etree
import re

base_url = "http://sh.lianjia.com"

if __name__ == "__main__":
    second_hand_url = "http://sh.lianjia.com/ershoufang"

    response = requests.get(second_hand_url)
    html = response.content

    # soup = BeautifulSoup(html)
    root = etree.HTML(html)
    print root

    xpath_str = '//*[@id="filter-options"]/dl[1]/dd/div/a'
    links = root.xpath(xpath_str)
    sum = 0
    # print links
    for link in links:
        sub_qu = base_url + link.attrib['href']
        response = requests.get(sub_qu)
        html = response.content
        root = etree.HTML(html)
        xpath_str = '//*[@id="filter-options"]/dl[1]/dd/div[2]/a'
        sub_links = root.xpath(xpath_str)
        for sub_link in sub_links:
            print base_url + sub_link.attrib['href']
            sum += 1

    print sum






