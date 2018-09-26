#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : EasyFile.py
# @Author: MoonKuma
# @Date  : 2018/9/25
# @Desc  : Methods in manipulating files

import os
import re

class EasyFile:

    def __init__(self):
        return

    def __modify(self, string):
        return str(string)

    def result_path(self):
        return os.path.abspath('.')

    def result_file_list(self):
        return os.listdir('.')

    def new_file(self, file_name):
        if file_name in self.result_file_list():
            print('Files', file_name, 'already exist, overwrite automatically')
        file_handle = open(os.path.join(self.result_path(), file_name), 'w', encoding='utf-8')
        return file_handle

    def new_file_safe(self, file_name):
        if file_name in self.result_file_list():
            print('Files', file_name, 'already exist, throw runtime error')
            raise RuntimeError('Duplicated files')
        else:
            file_handle = open(os.path.join(self.result_path(), file_name), 'w', encoding='utf-8')
            return file_handle

    def file_write(self, data_list, delimiter, file_handle):
        # write each data list in a line, adding /n in the end of each line, also surround non-number string with \'\'
        if len(data_list):
            data_str = self.__modify(data_list[0])
            for i in range(1,len(data_list)):
                data_str = data_str + delimiter + self.__modify(data_list[i])
            data_str = data_str + '\n'
            file_handle.write(data_str)


