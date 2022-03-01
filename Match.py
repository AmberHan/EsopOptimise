# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/3/1 16:18
# !@Author : DongHan Yang
# !@File   : Match.py
import copy


class Match:
    def __init__(self, fKey, gatesList):
        self.oldGates = gatesList
        self.fKey = fKey
        self.retGates = copy.deepcopy(gatesList)

    # 返回[(29, 15, 0), (17, 3, 0)...]
    def solveGates(self):
        g = self.oldGates
        key = self.fKey
        