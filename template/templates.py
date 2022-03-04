# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/2/24 14:15
# !@Author : DongHan Yang
# !@File   : templates.py

from template.cpmn import *


class MCT:
    def __init__(self, tup, n):
        key = tup[0]
        value = tup[1]
        targ = tup[2]
        self.key = key
        self.value = value
        self.targ = targ
        self.n = n
        self.cost = self.calCost(key, value)

    # 返回元组格式
    def getTup(self):
        return (self.key, self.value, self.targ)

    def calCost(self, key, value):
        qc = 0
        cost0 = [1, 1, 5, 13, 29, 61, 125, 253, 509, 1021]
        cost1 = [1, 1, 5, 13, 29, 52, 80, 100, 128, 152]
        cost2 = [1, 1, 5, 13, 26, 38, 50, 62, 74, 86]
        cNums = bin(key).count('1')
        if self.n - cNums >= cNums - 2:
            if cNums <= 9:
                qc = cost2[cNums]
            else:
                qc = 2 ** (cNums + 1) - 3
        elif self.n - cNums >= 1:
            if cNums <= 9:
                qc = cost1[cNums]
            else:
                qc = 24 * (cNums + 1) - 88
        else:
            if cNums <= 9:
                qc = cost0[cNums]
            else:
                qc = 12 * (cNums + 1) - 34
        if value == 0 and cNums != 0:
            qc += 2
        return qc


class templateMatch:
    def __init__(self, MCT1, MCT2, n):
        key1 = MCT1.key
        key2 = MCT2.key
        value1 = MCT1.value
        value2 = MCT2.value
        self.n = n
        if bin(key1).count('1') > bin(key2).count('1'):
            self.MCT1, self.MCT2, self.key1, self.key2, self.value1, self.value2 = \
                MCT1, MCT2, key1, key2, value1, value2
        else:
            self.MCT1, self.MCT2, self.key1, self.key2, self.value1, self.value2 = \
                MCT2, MCT1, key2, key1, value2, value1
        # self.MCT1 = MCT1 if bin(key1).count('1') > bin(key2).count('1') else MCT2
        # self.MCT2 = MCT2 if bin(key1).count('1') > bin(key2).count('1') else MCT1
        # self.key1 = self.MCT1.key
        # self.key2 = self.MCT2.key
        # self.value1 = self.MCT1.value
        # self.value2 = self.MCT2.value
        self.preCost = MCT1.cost + MCT2.cost
        self.finCost = 0
        self.reduceCost = 0
        self.retMCTList = []

    # 输入G1，G2，输出修改的
    # 满足模板1
    # if bin(M).count('1') + bin(N).count('1') == 1:
    def template1(self):
        big = self.key1
        x1 = self.value1
        small = self.key2
        y1 = self.value2
        _, P, M, N = getCpmn(big, x1, small, y1)
        if bin(P).count('1') == 0:
            # removeGates(small, y1, gates)
            cKey = M if M != 0 else N
            newValue = changeValue(cKey, big, x1)
            # changeGates(big, x1, newValue, gates)
            g1 = MCT((big, newValue, 0), self.n)
            self.setCost([g1])
            # self.finCost = g1.cost
            # self.reduceCost = self.preCost - self.finCost
            return [g1]

    # 满足模板2
    # if bin(M).count('1') + bin(N).count('1') == 1:
    def template2(self):
        big = self.key1
        x1 = self.value1
        small = self.key2
        y1 = self.value2
        _, P, M, N = getCpmn(big, x1, small, y1)
        if bin(P).count('1') == 1:
            cKey = M if M != 0 else N
            newValue = changeValue(cKey, big, x1)
            # changeGates(big, x1, newValue, gates)
            # removeGates(small, y1, gates)
            newKey = small ^ P
            newValue1 = retainKeyValue(newKey, small, y1)
            # putGates(newKey, newValue1, gates)
            g1 = MCT((big, newValue, 0), self.n)
            g2 = MCT((newKey, newValue1, 0), self.n)
            self.setCost([g1, g2])
            # self.finCost = g1.cost + g2.cost
            # self.reduceCost = self.preCost - self.finCost
            return [g1, g2]

    # 满足模板3
    # if bin(M).count('1') == 1 or bin(N).count('1') == 1:
    def template3(self):
        key1 = self.key1
        value1 = self.value1
        key2 = self.key2
        value2 = self.value2
        _, P, M, N = getCpmn(key1, value1, key2, value2)
        if bin(P).count('1') == 0:
            # 修改相对情况
            if bin(N).count('1') == 1:
                newM, newN, newKey1, newKey2, x1, y1 = M, N, key1, key2, value1, value2
            else:
                newM, newN, newKey1, newKey2, x1, y1 = N, M, key2, key1, value2, value1
            # newM = M if bin(N).count('1') == 1 else N
            # newN = N if bin(N).count('1') == 1 else M
            # newKey1 = key1 if newM == M else key2
            # newKey2 = key2 if newKey1 == key1 else key1
            # x1 = value1 if newKey1 == key1 else value2
            # y1 = value2 if x1 == value1 else value1
            # 从里面去除
            # removeGates(newKey1, x1, gates)  # g1
            # removeGates(newKey2, y1, gates)  # g2
            # 结构块放入结果
            newValueM = retainKeyValue(newM, newKey1, x1)
            toffi = MCT((newM, newValueM, newN), self.n)
            g3 = MCT((newKey2, y1, 0), self.n)
            # global setGate
            # setGate.extend([toffi, g3, toffi])
            # self.finCost = g3.cost + toffi.cost * 2
            # self.reduceCost = self.preCost - self.finCost
            self.setCost([toffi, g3, toffi])
            return [toffi, g3, toffi]

    # 满足模板4
    # if bin(M).count('1') == 1 and bin(N).count('1') == 1:
    def template4(self):
        key1 = self.key1
        value1 = self.value1
        key2 = self.key2
        value2 = self.value2
        _, P, M, N = getCpmn(key1, value1, key2, value2)
        if bin(P).count('1') == 1:
            # 从里面去除
            # removeGates(key1, value1, gates)  # g1
            # removeGates(key2, value2, gates)  # g2
            # g4
            newKey2 = key2 ^ P
            newValue2 = retainKeyValue(newKey2, key2, value2)
            g4 = MCT((newKey2, newValue2, 0), self.n)
            # toffi
            PM = P ^ M
            pmValue = retainKeyValue(PM, key1, value1)  # pm,pmvalue
            toffi = MCT((PM, pmValue, N), self.n)
            # cnot
            nValue = retainKeyValue(N, key2, value2)  # n,nvalue
            cnot = MCT((N, nValue, M), self.n)
            # global setGate
            # setGate.extend([cnot, toffi, g4, toffi, cnot])
            # self.finCost = g4.cost + cnot.cost * 2 + toffi * 2
            # self.reduceCost = self.preCost - self.finCost
            self.setCost([cnot, toffi, g4, toffi, cnot])
            return [cnot, toffi, g4, toffi, cnot]

    # 满足模板5
    def template5(self):
        key1 = self.key1
        value1 = self.value1
        key2 = self.key2
        value2 = self.value2
        # 符合T5，p=1
        # global inputN
        C, P, M, N = getCpmn(key1, value1, key2, value2)
        allKeys = C ^ P ^ M ^ N
        if bin(P).count('1') == 1 and bin(allKeys).count('1') < (1 << self.n) - 1:  # 有其他条件
            unUsed = ((1 << self.n) - 1) ^ allKeys
            u = unUsed & (-unUsed)  # target
            PM = P ^ M
            PN = P ^ N
            pmValue1 = retainKeyValue(PM, key1, value1)
            g1 = MCT((PM, pmValue1, u), self.n)
            pmValue2 = retainKeyValue(PN, key2, value2)
            g3 = MCT((PN, pmValue2, u), self.n)
            Cu = C ^ u
            cuValue = insertKeyValue(Cu, key1, value1)
            g2 = MCT((Cu, cuValue, 0), self.n)

            # global setGate
            # setGate.extend([g1, g2, g1, g3, g2, g3])
            self.setCost([g1, g2, g1, g3, g2, g3])
            return [g1, g2, g1, g3, g2, g3]

    # 满足模板6
    def template6(self):
        key1 = self.key1
        value1 = self.value1
        key2 = self.key2
        value2 = self.value2
        C, P, M, N = getCpmn(key1, value1, key2, value2)
        if bin(P).count('1') > 1:  # 有其他条件
            # 确定P最低位1
            P0 = P & (-P)
            pValue = retainKeyValue(P0, key1, value1)
            print(f'pValue一位:', pValue)
            if pValue == 1:
                newKey1, newKey2, newValue1, newValue2 = key1, key2, value1, value2
                g4 = self.MCT2
            else:
                newKey1, newKey2, newValue1, newValue2 = key2, key1, value2, value1
                g4 = self.MCT1
            # newKey1 = key1 if pValue == 1 else key2  # 错误
            # newKey2 = key2 if pValue == 1 else key1
            # newValue1 = value1 if newKey1 == key1 else value2  # 错误
            # newValue2 = value2 if value1 == newValue1 else value1
            # P最高位置为0
            #  newKey1,value3
            P3 = P ^ P0
            value3 = changeValue(P3, newKey1, newValue1)
            g3 = MCT((newKey1, value3, 0), self.n)
            # g4 = self.MCT1 if newKey1 == self.key1 else self.MCT2
            # newKey2,newValue2
            conutP3 = P3
            cnotList = []
            while conutP3:
                pLow = conutP3 & (-conutP3)
                g = MCT((P0, 1, pLow), self.n)
                conutP3 &= (conutP3 - 1)
                cnotList.append(g)
            # 原来的移除
            # removeGates(key1, value1, gates)  # g1
            # removeGates(key2, value2, gates)  # g2
            # 新增的
            # global setGate
            # setGate.extend(cnotList)
            retList = []
            retList.extend(cnotList)
            # 再对G1和G2进一步优化(C2,P0,M,N)
            p3 = templateMatch(g3, g4, self.n)
            opt = p3.template6Optimize()
            if opt is None:
                return []
            retList.extend(opt)
            retList.extend(cnotList)
            # self.finCost = opt.cost + len(cnotList) * 2 + p3.cost
            # self.reduceCost = self.preCost - self.finCost
            self.setCost(retList)
            return retList
            # setGate.extend(cnotList)

    def template6Optimize(self):
        key1 = self.key1
        value1 = self.value1
        key2 = self.key2
        value2 = self.value2
        C, P, M, N = getCpmn(key1, value1, key2, value2)
        if bin(M).count('1') == 0 and bin(N).count('1') == 0:
            rValue = retainKeyValue(C, key1, value1)
            ret = MCT((C, rValue, 0), self.n)
            self.finCost = ret.cost
            self.reduceCost = self.preCost - self.finCost
            return [MCT((C, rValue, 0), self.n)]
        elif bin(M).count('1') + bin(N).count('1') == 1:
            return self.template2()
        elif bin(M).count('1') == 1 and bin(N).count('1') == 1:
            return self.template4()
        elif P ^ M ^ N ^ C < (1 << self.n) - 1:
            return self.template5()

    def optimize12(self):
        key1 = self.key1
        value1 = self.value1
        key2 = self.key2
        value2 = self.value2
        C, P, M, N = getCpmn(key1, value1, key2, value2)
        if (bin(M).count('1') == 1 or bin(N).count('1') == 1) and bin(P).count('1') == 0 \
                and (bin(M).count('1') != 0 or bin(N).count('1') != 0):
            self.retMCTList = self.template3()
        elif bin(M).count('1') == 1 and bin(N).count('1') == 1 and \
                bin(P).count('1') == 1:
            self.retMCTList = self.template4()

    def optimize6(self):
        return self.template6()


    # 未使用自动化匹配
    def optimize(self):
        key1 = self.key1
        value1 = self.value1
        key2 = self.key2
        value2 = self.value2
        C, P, M, N = getCpmn(key1, value1, key2, value2)
        allKeys = C ^ P ^ M ^ N
        if bin(M).count('1') + bin(N).count('1') == 1 and bin(P).count('1') == 0:
            return self.template1()
        elif bin(M).count('1') + bin(N).count('1') == 1 and bin(P).count('1') == 1:
            return self.template2()
        elif bin(M).count('1') == 1 or bin(N).count('1') == 1 and \
                (bin(M).count('1') != 0 and bin(N).count('1') != 0) and bin(P).count('1') == 0:
            return self.template3()
        elif type == 4 and bin(M).count('1') == 1 and bin(N).count('1') == 1 and \
                bin(P).count('1') == 1:
            return self.template4()
        elif type == 5 and (bin(M).count('1') == 1 or bin(N).count('1') == 1) \
                and bin(P).count('1') == 1 and bin(allKeys).count('1') < self.n:
            return self.template5()
        elif type == 6 and bin(M).count('1') == 1 and bin(N).count('1') == 1:
            return self.template6()

    def setCost(self, gatesList):
        sumCost = 0
        for g in gatesList:
            sumCost += g.cost
        self.finCost = sumCost
        self.reduceCost = self.preCost - self.finCost


# # gates放入新值
# def putGates(newKey, newValue, gates):
#     if newKey in gates:  # 去重
#         if newValue not in gates[newKey]:
#             gates[newKey].append(newValue)
#         else:
#             gates[newKey].remove(newValue)
#     else:
#         gates[newKey] = [newValue]
#
#
# # gates改变值
# def changeGates(newKey, oldValue, newValue, gates):
#     if newValue in gates[newKey]:
#         gates[newKey].remove(newValue)
#     else:
#         gates[newKey].remove(oldValue)
#         gates[newKey].append(newValue)
#
#
# # gates删除值
# def removeGates(Key, Value, gates):
#     gates[Key].remove(Value)
#     if len(gates[Key]) == 0:
#         del gates[Key]
if __name__ == '__main__':
    n = 4
    # MCT1 = MCT((0b1111, 11, 0), n)
    # MCT2 = MCT((0b1101, 5, 0), n)
    # t = templateMatch(MCT1, MCT2, n)
    # g = t.template1()

    # MCT1 = MCT((0b1111, 15, 0), n)
    # MCT2 = MCT((0b1101, 5, 0), n)
    # t = templateMatch(MCT1, MCT2, n)
    # g = t.template2()

    # MCT1 = MCT((0b11110, 15, 0), 5)
    # MCT2 = MCT((0b11001, 7, 0), 5)
    # t = templateMatch(MCT1, MCT2, 5)
    # g = t.template3()

    # MCT1 = MCT((0b11110, 15, 0), 5)
    # MCT2 = MCT((0b11101, 13, 0), 5)
    # t = templateMatch(MCT1, MCT2, 5)
    # g = t.template4()

    # MCT1 = MCT((0b11111000, 15, 0), 8)
    # MCT2 = MCT((0b11100110, 11, 0), 8)
    # t = templateMatch(MCT1, MCT2, 8)
    # g = t.template5()

    # M,N为空
    # MCT1 = MCT((0b1111, 10, 0), 4)
    # MCT2 = MCT((0b1111, 5, 0), 4)
    # t = templateMatch(MCT1, MCT2, 4)
    # g = t.template6()

    # M有一个为空
    # MCT1 = MCT((0b11111, 26, 0), 5)
    # MCT2 = MCT((0b01111, 5, 0), 5)
    # t = templateMatch(MCT1, MCT2, 5)
    # g = t.template6()

    # M有均只有1个
    # MCT1 = MCT((0b10111, 10, 0), 5)
    # MCT2 = MCT((0b01111, 5, 0), 5)
    # t = templateMatch(MCT1, MCT2, 5)
    # g = t.template6()

    # 需要限制条件
    # MCT1 = MCT((0b110011, 10, 0), 7)
    # MCT2 = MCT((0b001111, 5, 0), 7)
    # t = templateMatch(MCT1, MCT2, 7)
    # g = t.template6()
    # print(1)
