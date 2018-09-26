#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : nga_popular_topic.py
# @Author: MoonKuma
# @Date  : 2018/9/25
# @Desc  : Collect popular topics from bbs.nga.cn
#          This is an example for 1. accessing html which require account information(cookie)
#                                 2. using beautifulsoup to dissect html elements

from bs4 import BeautifulSoup
import urllib.request
import time
import utils.EasyFile as EasyFile
import collections
import random


fid_map = {
    '-7': '大漩涡',
    '334': '硬件配置',
    '7': '艾泽拉斯议事厅',
    '321': 'dota2',
    '540': 'fgo',
    '549': '崩坏3',
    '538': '阴阳师',
}

cookie = 'ngaPassportUid=guest05baafb076ae25; UM_distinctid=16613e4953246d-06d111daddb079-333b5602-1fa400-16613e495339e4; taihe=e91da2285c4f9c0d77659a8af63752f9; Hm_lvt_5adc78329e14807f050ce131992ae69b=1537932040; CNZZDATA1256638903=688248958-1537941967-http%253A%252F%252Fbbs.nga.cn%252F%7C1537941967; CNZZDATA1256638820=1978580750-1537940918-http%253A%252F%252Fbbs.nga.cn%252F%7C1537946318; CNZZDATA1256638919=1949833754-1537947823-http%253A%252F%252Fbbs.nga.cn%252F%7C1537947823; CNZZDATA30043604=cnzz_eid%3D414827177-1537927474-%26ntime%3D1537949074; bbsmisccookies=%7B%22insad_refreshid%22%3A%7B0%3A%22/153794231025962%22%2C1%3A1538549729%7D%2C%22pv_count_for_insad%22%3A%7B0%3A-40%2C1%3A1537981258%7D%2C%22insad_views%22%3A%7B0%3A1%2C1%3A1537981258%7D%7D; Hm_lpvt_5adc78329e14807f050ce131992ae69b=1537949806; lastvisit=1537950499; guestJs=1537950499; CNZZDATA30039253=cnzz_eid%3D1732079848-1537928258-%26ntime%3D1537949858'
ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' \
     '69.0.3497.100 Safari/537.36'
header = {'User-Agent': ua, 'Cookie': cookie}
page_limit = 10
url = 'http://bbs.nga.cn/thread.php?fid={}&page={}&rand={}'  # url.format('7','1','121')
easy_file = EasyFile.EasyFile()


def read_html(html, data_dict):
    req = urllib.request.Request(html, headers=header)
    res = urllib.request.urlopen(req)
    soup = BeautifulSoup(res, "html.parser")
    t_body_list = soup.find_all('tbody')
    item_id = 1
    for t_body in t_body_list:
        counts = t_body.find('td', attrs={'class': 'c1'}).get_text()
        topic = '\'' + t_body.find('td', attrs={'class': 'c2'}).get_text().strip().replace('\n', '').replace(',', '，') + '\''
        post_time_unix = t_body.find('td', attrs={'class': 'c3'}).find('span').get_text()
        post_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(post_time_unix)))
        data_dict[item_id] = dict()
        data_dict[item_id]['counts'] = counts
        data_dict[item_id]['topic'] = topic
        data_dict[item_id]['post_time'] = post_time
        item_id += 1


def check_topic():
    global page_limit
    global url
    result_dict = collections.OrderedDict()
    for fid in fid_map.keys():
        result_dict[fid] = collections.OrderedDict()
        result_dict[fid]['name'] = fid_map.get(fid)
        result_dict[fid]['content'] = collections.OrderedDict()
        for page_id in range(1, page_limit+1):
            rand = random.randint(100,999)
            html = url.format(str(fid), str(page_id), str(rand))
            print(html)
            result_dict[fid]['content'][page_id] = collections.OrderedDict()
            read_html(html, result_dict[fid]['content'][page_id])
    file_name = 'nga_topics_' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.txt'
    file_save = easy_file.new_file(file_name)
    head_line = ['论坛名称', '页', '话题', '楼层数', '发表时间']
    easy_file.file_write(head_line, ',', file_save)
    for fid in result_dict.keys():
        name = result_dict[fid]['name']
        content = result_dict[fid]['content']
        for page_id in content.keys():
            page = content[page_id]
            for item in page.keys():
                data_line = list()
                data_line.append(name)
                data_line.append(page_id)
                data_line.append(page[item]['topic'])
                data_line.append(page[item]['counts'])
                data_line.append(page[item]['post_time'])
                easy_file.file_write(data_line, ',', file_save)
    file_save.close()


# test
check_topic()




