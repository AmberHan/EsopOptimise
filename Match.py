# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/3/1 16:18
# !@Author : DongHan Yang
# !@File   : Match.py
import copy
from template.oracleOptimse import myOracle
from template.templates import *


class Match:
    def __init__(self, fKey, gatesTupList, n, unused):
        # [(29, 15, 0), (17, 3, 0),...]
        self.oldGates = gatesTupList
        self.unused = unused
        self.fKey = fKey
        self.retGates = []
        self.n = n
        self.solveRetGatesList = []
        self.solveGates()

    # 返回[(29, 15, 0), (17, 3, 0)...]
    def solveGates(self):
        g = self.oldGates
        key = self.fKey
        # 第1个阶段匹配所有1和2
        g = myOracle(self.n, g)
        MCTList = []  # 需要维护MCTList
        # 类型转换，进入3456匹配
        for gateTup in g:
            MCTs = MCT((gateTup[0], gateTup[1], 0), self.n)
            MCTList.append(MCTs)
        # list类排序
        MCTList = sorted(MCTList, key=lambda box: box.key, reverse=True)
        # 第2个阶段匹配所有满足3和4；同时排序选择优化最大的
        retMctList34 = self.sloveMCTList(MCTList, 34)  # 得到34返回
        self.saveRetTup(retMctList34)  # 存储
        # 第3个阶段，进入6匹配
        retMctList6 = self.sloveMCTList(MCTList, 6)  # 得到6返回
        self.saveRetTup(retMctList6)  # 存储
        # 第3个阶段匹配所有满足5的
        retMctList5 = self.sloveMCTList(MCTList, 5)  # 得到5返回
        self.saveRetTup(retMctList5)  # 存储
        # 无匹配的附加
        self.saveRetTup(MCTList)  # 存储

    # 存储返回结果
    def saveRetTup(self, retMctList):
        if len(retMctList) != 0:
            retTupList = self.MctToTupList(retMctList)
            self.solveRetGatesList.extend(retTupList)

    # 删除MCTList所有匹配3456的模式， 返回匹配好的组合
    def sloveMCTList(self, MCTList, type):
        saveIndex = 0
        retMCTList = []
        while True:
            lenMct = len(MCTList)
            if saveIndex >= lenMct - 1 or lenMct == 0:
                break
            for i in range(saveIndex, lenMct):
                maxDecrease = 0
                mctIndex = -1
                if i == lenMct - 1:
                    saveIndex = lenMct - 1
                for j in range(i + 1, lenMct):
                    t = templateMatch(MCTList[i], MCTList[j], self.n, self.unused)
                    if type == 34:
                        t.optimize34()
                    elif type == 5:
                        t.optimize5()
                        # pass
                    elif type == 6:
                        # pass
                        t.optimize6()
                    if maxDecrease < t.reduceCost:
                        maxDecrease = t.reduceCost
                        mctIndex = j
                        mtt = t
                if mctIndex > -1:
                    if type == 6:
                        print("type6")
                    MCTList.remove(MCTList[mctIndex])
                    MCTList.remove(MCTList[i])
                    retMCTList.extend(mtt.retMCTList)
                    saveIndex = i
                    break
        return retMCTList

    # 格式转换：MCT列表转为元组列表
    def MctToTupList(self, MCTList):
        tupList = []
        for mctclass in MCTList:
            tupList.append(mctclass.getTup())
        return tupList
