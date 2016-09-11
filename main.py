# coding=utf-8

import requests
from bs4 import BeautifulSoup
import lxml
import re


if __name__ == "__main__":
    second_hand_url = "http://sh.lianjia.com/ershoufang/"

    response = requests.get(second_hand_url)
    html = response.content

    soup = BeautifulSoup(html)


