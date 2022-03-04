# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/2/26 18:29
# !@Author : DongHan Yang
# !@File   : oracle4bitOptimise.py
# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/1/25 17:03
# !@Author : DongHan Yang
# !@File   : Oracle-4qbit.py
import random
from template.mode1 import mode1
from template.mode2 import mode2
from template.jbBlossom import jb_blossom
import copy
import math


class Oracle:
    def __init__(self, n, gates):
        self.n = n
        self.fx2 = []
        self.oldGates = gates
        self.oldgc, self.oldqc = self.calCost(self.oldGates)
        self.midGates = self.oldGates
        self.retGates = {}
        self.optimize1()
        self.gc, self.qc = self.calCost(self.retGates)

    # 设置NOT
    def setNot(self):
        gates = copy.deepcopy(self.retGates)
        for key, values in gates.items():
            if bin(key).count('1') != 1:
                continue
            elif values[0] == 0:
                self.retGates[key][0] = 1
                self.putGates(0, [0], self.retGates)
        self.gc, self.qc = self.calCost(self.retGates)

    # 计算代价
    def calCost(self, gates):
        gc = 0
        qc = 0
        notsnum = 0
        cost0 = [1, 1, 5, 13, 29, 61, 125, 253, 509, 1021]
        cost1 = [1, 1, 5, 13, 29, 52, 80, 100, 128, 152]
        cost2 = [1, 1, 5, 13, 26, 38, 50, 62, 74, 86]
        for key, values in gates.items():
            cNums = bin(key).count('1')
            if self.n - cNums >= cNums - 2:
                if cNums <= 9:
                    vc = cost2[cNums]
                else:
                    vc = 2 ** (cNums + 1) - 3
            elif self.n - cNums >= 1:
                if cNums <= 9:
                    vc = cost1[cNums]
                else:
                    vc = 24 * (cNums + 1) - 88
            else:
                if cNums <= 9:
                    vc = cost0[cNums]
                else:
                    vc = 12 * (cNums + 1) - 34
            for value in values:
                gc += 1
                qc += vc
                if value == 0 and cNums != 0:
                    qc += 1
                    notsnum += 1
        if notsnum == 1:
            qc += 1
        return gc, qc

    # 如01(1)010, 010 对应倒数第2个1取反 -> 01(0)010
    # key:  1100 0101
    # valu1:01    0 1
    # valu2:11    1 1
    # count:10    1 0
    # index:00    1 0
    # outpu:1100 0001
    def get_key(self, key, index):
        c_key = key
        # 找到第2个1
        while index != 1:  # 清除1
            c_key &= (c_key - 1)
            index >>= 1
        new_key = (c_key & (-c_key)) ^ key
        return new_key

    # key: 得到1的数目
    # value:  1010
    # reomve: 0010 移除对应1的
    # output: 10 0
    def get_value(self, key, vaule, romove_value_index):
        count = bin(key).count('1')
        last_index = romove_value_index
        xor_value = (1 << count) - 1
        low = (last_index - 1) & vaule
        high = (vaule >> 1) & (xor_value ^ (last_index - 1))
        return low + high

    # 将key中的x1和x2合并，存入gates
    def merge(self, key, x1, x2):
        gates = self.retGates
        count = x1 ^ x2  # 获取1数目,是对应value的
        # 生成count个门
        while count:
            last_index = count & (-count)  # 获取最后一位1
            # value:二进制中间去掉一个值，得到新的二进制
            y1 = self.get_value(key, x1, last_index)
            # key:对应key的第last_index个1变成0
            new_key = self.get_key(key, last_index)
            # y2 = ((x1 >> 1) & (0b11111111 ^ (last_index - 1))) + ((last_index - 1) & x1)  # 保留last_index前后值，前面右移
            # new_key1 = getValueKey(key, ((1 << bin(key).count('1')) - 1) ^ last_index)
            # print(y1 == y2)
            # print(new_key == new_key1)
            self.putGates(new_key, [y1], gates)
            x1 ^= last_index  # 中间门态
            count &= (count - 1)  # 最后一位1清0

    # 存放门
    def putGates(self, key, valueList, gates):
        for value in valueList:
            if key in gates:
                # 偶数抵消
                if gates[key].count(value):
                    gates[key].remove(value)
                    if len(gates[key]) == 0:
                        del gates[key]
                else:
                    gates[key].append(value)
            else:
                gates[key] = [value]

    # 递归优化
    def optimize1(self):
        gates = self.midGates
        # 最近邻排序
        # jb_blossom(self.midGates)
        # 存放新的new_gates
        self.retGates = {}
        is_ret = True
        for key, value in gates.items():
            if len(value) % 2 == 1:  # 奇数最后一位不好处理
                self.putGates(key, [value[-1]], self.retGates)
            # 偶数个
            for i in range(len(value) // 2):
                a, b = value[i * 2], value[2 * i + 1]
                # 超过分解代价高
                if bin(a ^ b).count('1') >= 10:
                    lenv = len(value) if len(value) % 2 == 0 else len(value) - 1
                    self.putGates(key, value[i * 2: lenv], self.retGates)
                    break
                else:
                    is_ret = False
                    self.merge(key, a, b)  # 两两合并
        # print(f'中间生成态',self.retGates)
        if is_ret:
            return
        self.midGates = copy.deepcopy(self.retGates)
        self.optimize1()


def dictEqu(g1, g2):
    for key, value in g1.items():
        if key not in g2:
            return False
        else:
            for v in value:
                if v not in g2[key]:
                    return False
    return True


def listToDic(tupList):
    keyValue = {}
    for tup in tupList:
        key = tup[0]
        value = tup[1]
        if key in keyValue:
            keyValue[key].append(value)
        else:
            keyValue[key] = ([value])
    return keyValue


def dicToTup(keyValue):
    tupList = []
    for key, values in keyValue.items():
        for value in values:
            tupList.append((key, value, 0))
    return tupList


def myOracle(n, tupList):
    g = listToDic(tupList)
    while True:
        gg = copy.deepcopy(g)
        g1 = Oracle(n, g)
        g2 = mode1(g1.retGates)
        g = mode2(g2)
        if dictEqu(g, gg) and dictEqu(gg, g2):
            break
    g1.setNot()
    print(f'阶段1局部后：', g)
    print(g1.qc, g1.gc)
    return dicToTup(g1.retGates)


if __name__ == '__main__':
    n = 5
    gates = {118: [18], 86: [10]}
    myOracle(n, gates)
    print("*" * 100)
