#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。

import unittest
from lib.utility.date import *


class DateTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_time_string(self):
        self.assertEqual(len(get_time_string()), 14)

    def test_date_string(self):
        self.assertEqual(len(get_date_string()), 8)

    def test_year_string(self):
        self.assertEqual(len(get_year_month_string()), 6)


if __name__ == '__main__':
    unittest.main()
