#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : fgo_wiki.py
# @Author: MoonKuma
# @Date  : 2018/9/25
# @Desc  : Characters' data from fgo-wiki ( regular expression )

import re
import urllib
import json
import time
import utils.EasyFile as EasyFile


attributeList = ['ID', 'NAME', 'NAME_EN', 'STAR', 'CLASS', 'Gender', 'ILLUST', 'CV', 'Origin', 'Region', 'Camp',
                 'T_NAME', 'T_PROP', 'T_TYPE']
picStr = 'http://file.fgowiki.fgowiki.com/fgo/card/servant/'
urlStr = "http://fgowiki.com/guide/petdetail/"

# id_range(eg: range(0,223))


def get_character_info(character_list):
    global attributeList
    global picStr
    global urlStr
    easy_file = EasyFile.EasyFile()
    file_name = 'fgo_wiki_' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '_' + str(character_list[0]) + \
                '_' + str(character_list[len(character_list)-1]) + '.txt'
    file_save = easy_file.new_file(file_name)
    file_save.write('ID|NAME|NAME_EN|STAR|CLASS|Gender|ILLUST|CV|Origin|Region|Camp|T_NAME|T_PROP|T_TYPE\n')
    for character_id in character_list:
        data_str = ''
        url = urlStr + str(character_id)
        print(url)
        page = urllib.request.urlopen(url)
        html = page.read()
        html = html.decode('utf-8')
        reg = r'var datadetail = \[\{(.+?)\}\]\;'
        img_list = re.findall(reg, html)
        json_cont = img_list[0].strip()
        json_str = '{' + json_cont + '}'
        json_data = json.loads(json_str)
        for i in range(0, len(attributeList)):
            key = attributeList[i]
            value = json_data.setdefault(key, ' ')
            # try:
            #     value = str(value.encode('utf-8')) # this is useful only in python 2, python 3 use unicode
            # except:
            #     pass
            if i > 13:
                value = urlStr + value
            if i == 0:
                data_str = value
            else:
                data_str = data_str + '|' + value
        data_str = data_str + '\n'
        file_save.write(data_str)
    file_save.close()


# test
test_character_list = range(0, 223)
get_character_info(test_character_list)

