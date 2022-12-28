import os
import sys
import csv
import json
from collections import OrderedDict
from typing import List

from Singleton import Singleton


def get_input():
    args = [line for line in csv.reader([input(">>> ").replace('\'', '\"')],
                                        skipinitialspace=True, delimiter=' ')][0]
    return [arg.replace('\'', '').replace('\"', '') for arg in args]


def get_fault_and_content():
    instance = Singleton.getInstance()
    lst = instance.get_dict_data_select("""select * from fault;""")
    prt = "，".join(["%s报修请按\'%d\'" % (dct['fault_name'], i + 1) for i, dct in enumerate(lst)])
    fault_name = lst[int(input(prt + '：\n>>>')) - 1]['fault_name']
    repair_content = input("请大致描述下需要报修的内容：\n>>>")
    return fault_name, repair_content


def update_sys_argv(new_argv):
    sys.argv = [sys.argv[0]]
    sys.argv.extend(new_argv)


def every(lst, fn=lambda x: x):
    return all(map(fn, lst))


def get_cur_root_and_name():
    path = os.getcwd().replace('\\', '/')
    name = path.split('/')[-1]
    root = '/'.join(path.split('/')[:-1])
    return name, root

