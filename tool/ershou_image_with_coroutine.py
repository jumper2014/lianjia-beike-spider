#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 协程下载图片，仅支持Python 3.6.1



import aiohttp
import aiofiles
import asyncio
import os
import time
from lib.zone.city import get_chinese_city
from lib.request.headers import create_headers
from lib.utility.date import get_date_string
from lib.spider.base_spider import SPIDER_NAME
from lib.utility.path import DATA_PATH


def get_ershou_img_urls(city):
    urls = list()
    date = get_date_string()
    # 获得 csv 文件路径
    # date = "20180331"   # 指定采集数据的日期
    # city = "sh"         # 指定采集数据的城市
    csv_dir = "{0}/{1}/ershou/{2}/{3}".format(DATA_PATH, SPIDER_NAME, city, date)

    files = list()
    if not os.path.exists(csv_dir):
        print("{0} does not exist.".format(csv_dir))
        print("Please run 'python ershou.py' firstly.")
        print("Bye.")
        exit(0)
    else:
        print('OK, start to process ' + get_chinese_city(city))
    for csv in os.listdir(csv_dir):
        if csv[-3:] != "csv":
            continue
        data_csv = csv_dir + "/" + csv
        # print(data_csv)
        files.append(data_csv)

    # 清理数据
    count = 0
    for csv in files:
        with open(csv, 'r') as f:
            for line in f:
                count += 1
                text = line.strip()
                try:
                   results = text.split("https://")
                except Exception as e:
                    print(text)
                    print(e)
                    continue
                # 确保之前的步骤采集到了图片的url
                if len(results) > 1:
                    url = results[-1]
                    urls.append("https://"+url)
                    print("https://"+url)
    print(len(urls))
    return urls


async def download_images(save_path: str, image_url: str):
    """
    :param save_path: 保存图片的路径
     :param image_url: 图片的下载的url地址
    :return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url, headers=create_headers()) as req:
            image = await req.read()
            fp = await aiofiles.open(save_path, 'wb')
            await fp.write(image)

if __name__ == '__main__':
    # urls = ["https://img.ljcdn.com/370600-inspection/test-9925c97c-fc99-4d1a-97fa-2fd6d3209027.png!m_fill,w_280,h_210,f_jpg?from=ke.com",
    #         "https://img.ljcdn.com/370600-inspection/df98f65c-427e-4d7d-91a7-425a5d682af5.jpg!m_fill,w_280,h_210,f_jpg?from=ke.com",
    #         "https://img.ljcdn.com/370600-inspection/test-9925c97c-fc99-4d1a-97fa-2fd6d3209027.png!m_fill,w_280,h_210,f_jpg?from=ke.com",
    #         "https://img.ljcdn.com/370600-inspection/df98f65c-427e-4d7d-91a7-425a5d682af5.jpg!m_fill,w_280,h_210,f_jpg?from=ke.com"]
    # 指定城市
    start = time.time()
    city = "yt"
    urls = get_ershou_img_urls(city)
    loop = asyncio.get_event_loop()
    date = get_date_string()
    csv_dir = "{0}/{1}/ershou/{2}/{3}".format(DATA_PATH, SPIDER_NAME, city, date)
    to_do = [download_images("{0}/{1}.jpg".format(csv_dir, i), urls[i]) for i in range(len(urls))]
    print("Start to download, please wait.")
    wait_future = asyncio.wait(to_do)
    resp = loop.run_until_complete(wait_future)
    loop.close()
    print("Download {0} images, cost {1} seconds.".format(len(urls), time.time() - start))
