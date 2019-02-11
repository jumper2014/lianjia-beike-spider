#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 用于获取代理

from bs4 import BeautifulSoup
import requests
from lib.request.headers import create_headers

proxys_src = []
proxys = []


def spider_proxyip(num=10):
    try:
        url = 'http://www.xicidaili.com/nt/1'
        req = requests.get(url, headers=create_headers())
        source_code = req.content
        print(source_code)
        soup = BeautifulSoup(source_code, 'lxml')
        ips = soup.findAll('tr')

        for x in range(1, len(ips)):
            ip = ips[x]
            tds = ip.findAll("td")
            proxy_host = "{0}://".format(tds[5].contents[0]) + tds[1].contents[0] + ":" + tds[2].contents[0]
            proxy_temp = {tds[5].contents[0]: proxy_host}
            proxys_src.append(proxy_temp)
            if x >= num:
                break
    except Exception as e:
        print("spider_proxyip exception:")
        print(e)


if __name__ == '__main__':
    spider_proxyip(10)
    print(proxys_src)
