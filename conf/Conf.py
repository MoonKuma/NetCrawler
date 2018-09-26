#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : Conf.py
# @Author: MoonKuma
# @Date  : 2018/9/25
# @Desc  : config parameters


class Conf:
    def __init__(self):
        self.mongo_conf = dict()
        self.path = dict()
        self.load()

    def load(self):
        # mongo_db_conf
        self.mongo_conf['url'] = '192.168.2.175'
        self.mongo_conf['db'] = 'gmt_test'

    def show_component(self):
        co_list = list(self.__init__.func_code.co_names)
        co_list.remove('dict')
        co_list.remove('load')
        return co_list

    def show_details(self, *component_name):
        obj = Conf()
        if len(component_name) > 0:
            print(component_name[0], ':', getattr(obj, component_name[0], 'not found'))
            return
        co_list = self.show_component()
        for component in co_list:
            print(component, ':', getattr(obj, component, 'not found'))