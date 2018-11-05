#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 协程下载图片，Python 3.6.1


import aiohttp
import aiofiles
import asyncio
from lib.request.headers import create_headers


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
    urls = ["https://img.ljcdn.com/370600-inspection/test-9925c97c-fc99-4d1a-97fa-2fd6d3209027.png!m_fill,w_280,h_210,f_jpg?from=ke.com",
            "https://img.ljcdn.com/370600-inspection/df98f65c-427e-4d7d-91a7-425a5d682af5.jpg!m_fill,w_280,h_210,f_jpg?from=ke.com",
            "https://img.ljcdn.com/370600-inspection/test-9925c97c-fc99-4d1a-97fa-2fd6d3209027.png!m_fill,w_280,h_210,f_jpg?from=ke.com",
            "https://img.ljcdn.com/370600-inspection/df98f65c-427e-4d7d-91a7-425a5d682af5.jpg!m_fill,w_280,h_210,f_jpg?from=ke.com"]

    loop = asyncio.get_event_loop()
    to_do = [download_images("{0}.jpg".format(i), urls[i]) for i in range(len(urls))]
    wait_future = asyncio.wait(to_do)
    resp, _ = loop.run_until_complete(wait_future)
    loop.close()
