# coding=utf-8
# author: yuetian

import requests
from bs4 import BeautifulSoup
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
            if sub_link not in urls:
                urls.append(sub_link)
    return urls


def get_xiaoqu_info():
    page = 'http://sh.lianjia.com/xiaoqu/beicai/'
    response = requests.get(page)
    html = response.content
    soup = BeautifulSoup(html, "lxml")
    # houselist_elem = soup.find(id='house-lst')
    house_elems = soup.find_all('div', class_="info-panel")
    for house_elem in house_elems:
        price = house_elem.find('span', class_="num")
        name = house_elem.find('h2')
        sale = house_elem.select('div[class="square"] > div > a > span')


        print price.text.strip() + "," + name.text.replace("\n", "") + "," + sale[0].text

    last_page = soup.find('a', gahref="results_totalpage")
    print last_page.text

    # print house_elems





if __name__ == "__main__":
    # urls = get_xiaoqu_bankuai_urls()
    # print urls
    get_xiaoqu_info()


