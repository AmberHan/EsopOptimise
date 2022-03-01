# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/3/1 9:24
# !@Author : DongHan Yang
# !@File   : compares.py
import os.path


def getGates(fileName):
    with open(fileName, 'r') as f:
        content = f.readlines()
    f.close()
    return content


name = "dec.tfc"
name1 = "newdec.tfc"
path = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "benchmarks\\" + name
path1 = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "benchmarks\\" + name1
g = getGates(path)
# print(g)
g1 = getGates(path1)
# print(g1)
for gg in g1:
    if gg not in g:
        print(gg)
