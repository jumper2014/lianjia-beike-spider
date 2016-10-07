# coding=utf-8
# author: Zeng YueTian


import requests
from bs4 import BeautifulSoup
from lxml import etree
from lib.const.url import *
from lib.const.xpath import *
from lib.url.url_helper import *
from lib.city.xiaoqu import *
from lib.city.district import *


def get_xiaoqu_district_urls():
    """
    获取小区栏目下面的各区导航链接
    :return:
    """
    urls = get_urls_from_xpath(SH_XIAOQU_BASE_URL, XIAOQU_QU_XPATH)
    print urls
    return urls

def get_xiaoqu_district_url(district):
    """
    获取小区栏目下面的各区导航链接
    :return:
    """
    urls = get_urls_from_xpath(SH_XIAOQU_BASE_URL, XIAOQU_QU_XPATH)
    print urls
    return urls


def get_xiaoqu_area_urls():
    """
    获取小区栏目下面的各区下级板块导航链接
    :return:
    """
    urls = []
    for link in get_xiaoqu_district_urls():
        for sub_link in get_urls_from_xpath(link, XIAOQU_BANKUAI_XPATH):
            if sub_link not in urls:
                urls.append(sub_link)
    return urls


def get_xiaoqu_area(district):
    """
    获取小区栏目下面的各区下级板块导航链接
    :return:
    """
    areas = []
    for link in get_xiaoqu_district_urls():
        for sub_link in get_urls_from_xpath(link, XIAOQU_BANKUAI_XPATH):
            area = sub_link.split("/")[-1]
            if area not in areas:
                areas.append(area)
    return areas


def get_xiaoqu_info(city, area):
    district = AREA_DICT.get(area, "")
    chinese_district = get_chinese_district(district)
    chinese_area = CHINESE_AREA_DICT.get(area, "")
    xiaoqu_list = list()
    page = 'http://{0}.lianjia.com/xiaoqu/{1}/'.format(city, area)
    response = requests.get(page)
    html = response.content
    soup = BeautifulSoup(html, "lxml")

    # 获得总的页数
    total_page = 0
    last_page = soup.find('a', gahref="results_totalpage")
    if last_page is not None:  # 如果找到了标示最后一页的链接
        total_page = int(last_page.text)
    else:   # 没有标示最后一页的链接,那么总页数不超过10,从大到小倒序找到最后一页
        href_list = ["results_d{0}".format(i) for i in range(10+1)[1:]]
        href_list.reverse()
        for href in href_list:
            last_page = soup.find('a', gahref=href)
            if last_page is not None:
                total_page = int(last_page.text)
                break


    # 从第一页开始,一直遍历到最后一页
    for i in range(total_page+1)[1:]:
        page = 'http://{0}.lianjia.com/xiaoqu/{1}/d{2}'.format(city, area, i)
        # print page
        response = requests.get(page)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得有小区信息的panel
        house_elems = soup.find_all('div', class_="info-panel")
        for house_elem in house_elems:
            price = house_elem.find('span', class_="num")
            name = house_elem.find('h2')
            on_sale = house_elem.select('div[class="square"] > div > a > span')

            # 继续清理数据
            price = price.text.strip()
            name = name.text.replace("\n", "")
            on_sale = on_sale[0].text.strip()

            # 作为对象保存
            xiaoqu = XiaoQu(chinese_district, chinese_area, name, price, on_sale)
            xiaoqu_list.append(xiaoqu)
            # print price, name, on_sale
    return xiaoqu_list


if __name__ == "__main__":
    # urls = get_xiaoqu_area_urls()
    # print urls
    get_xiaoqu_info("sh", "beicai")


