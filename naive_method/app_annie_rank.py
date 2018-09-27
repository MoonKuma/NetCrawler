#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : app_annie_rank.py
# @Author: MoonKuma
# @Date  : 2018/9/27
# @Desc  : Collect ranking data from App Annie
#          This is an example for: 1. collecting AJAX (Asynchronous Javascript And XML) data
#                                  2. solving anti-crawler mechanism （in a rather rough way）

import urllib.request
import json
import time
import random
from utils.Tools import get_date_list, get_today
import utils.EasyFile as EasyFile

date_format = '%Y-%m-%d'
start_date = '2018-01-01'
end_date = get_today(date_format)
date_list = get_date_list(start_date, end_date, date_format)
file_name = 'app_annie_'  + end_date + '.txt'
file_save = EasyFile.EasyFile().new_file_safe(file_name)

# rewrite cookie here
cookie = r'aa_language=cn; rid=ecb645894eaa45808c288977645345d5; csrftoken=YBVHS62LssgDAibESOTd3Sv4kStdR43t; _ga=GA1.2.1534735255.1526554550; _mkto_trk=id:071-QED-284&token:_mch-appannie.com-1526554552592-55156; _tdim=e23087a8-9aaf-4bf9-8772-12f8d379f17a; wcs_bt=s_14249a956b4d:1526627812; _gcl_au=1.1.236243710.1537510821; _gid=GA1.2.1199722969.1538016108; django_language=zh-cn; _gat_UA-2339266-6=1; sessionId=".eJxNzUFKA0EQheF2jFFHg8YsvYBuRs9gVhrMIligq6amu0iatDXTU9VKBMGVkNN4J08igSjufh58vI_iPe1cwFBIJDTcUidBlFjXMNhuVhQ7nRg4iMjzjHN6LIwxjmFgMevCZqHOBn83fBoZOPlVxFhH8pMCeijBT-FIG7G59ajkU7GGs3-6Rrck9nD9SjUyxpUGJxU612TWaoxCtyzEEjS80H3jKd5sxSlG6tS6Bbml1fBMbnOwifIv0i6U-9-H5_3R1XHz5dqVvpUWHsZl6l3O0t7nLPVz9QOjX13-:1g5PeO:-JrpvLUcHj7vfgT0jiCmjfZiTvc"; aa_user_token=".eJxrYKotZNQI5SxNLqmIz0gszihkClVINLQ0S7NISTZNsjA2t0yztDRKNrRMNjMzTzVOMzYySwsVik8sLcmILy1OLYpPSkzOTs1LKWQONShPTUrMS8ypLMlMLtZLTE7OL80r0XNOLE71zCtOzSvOLMksS_XNT0nNcYLqYQnlRTIpM6WQ1UswUpihVA8AuJQzGA:1g5Peh:HUnx2-iRjdgOLd_iu6fyAgAHYUc"'

for date_str in date_list:
    try:
        url = 'https://www.appannie.com/ajax/top-chart/table/?market=ios&country_code=CN&category=36&date='+date_str+r'&rank_sorting_type=rank&page_size=100&order_type=desc&device=iphone'
        cookie_str = cookie
        refer_str = r'https://www.appannie.com/apps/ios/top-chart/?country=CN&category=36&device=iphone&date=='+date_str+r'&feed=All&rank_sorting_type=rank&page_number=0&page_size=100&table_selections='
        req = urllib.request.Request(url)
        req.add_header('cookie', cookie_str)
        # req.add_header(':authority', 'www.appannie.com')
        # req.add_header(':method', 'GET')
        # req.add_header(':path', '/ajax/top-chart/table/?market=google-play&country_code=JP&category=1&date='+date_str+r'&rank_sorting_type=rank&page_size=100&order_by=sort_order&order_type=desc&feed=Grossing')
        # req.add_header(':scheme', 'https')
        # req.add_header('accept', 'application/json, text/plain, */*')
        # req.add_header('accept-language', 'zh-CN,zh;q=0.8')
        req.add_header('referer', refer_str)
        req.add_header('user-agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')
        # req.add_header('x-csrftoken', 'jYwTsbFrTlon05Tt2dGkeo40cRir0bcE')
        # req.add_header('x-newrelic-id', 'VwcPUFJXGwEBUlJSDgc=')
        # req.add_header('x-requested-with', 'XMLHttpRequest')
        r = urllib.request.urlopen(req)
        json_str = r.read().decode('utf-8')
        jsonData = json.loads(json_str)
        jsonData_table = jsonData['table']
        jsonData_table_row = jsonData_table['rows']
        for row_item in jsonData_table_row:
            str_2_wri = date_str
            rank = row_item[0]
            str_2_wri = str_2_wri + '||' + str(rank)
            data_dict = row_item[1][0]
            game_name = data_dict[u'name'].encode('utf-8')
            company_name = data_dict[u'company_name'].encode('utf-8')
            game_type = row_item[8].encode('utf-8')
            game_score = round(row_item[9][0],2)
            game_reg = row_item[11][0].encode('utf-8')
            str_2_wri = str_2_wri + '||' + str(game_name) + '||' + str(company_name) + '||' + str(game_type) + '||' + str(game_score) + '||'  + str(game_reg)
            str_2_wri = str_2_wri + '\n'
            file_save.write(str_2_wri)
    except:
        print('Error in date:', date_str)
    finally:
        time.sleep(2 + random.randint(1, 1000)/333.0)