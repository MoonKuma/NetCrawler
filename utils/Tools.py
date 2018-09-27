#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : Tools.py
# @Author: MoonKuma
# @Date  : 2018/9/27
# @Desc  : Some Useful Tools

import datetime
import time


def get_date_list(start_date, end_date, date_format):
    # date_list
    date_list = list()
    d1 = datetime.datetime.strptime(start_date, date_format)
    d2 = datetime.datetime.strptime(end_date, date_format)
    day_diff = (d2 - d1).days
    while day_diff >= 0:
        date_list.append(d1.strftime(date_format))
        d1 = d1 + datetime.timedelta(days=1)
        day_diff = (d2 - d1).days
    return date_list


def get_today(date_format):
    # today
    return time.strftime(date_format, time.localtime(time.time()))