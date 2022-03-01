# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/2/24 14:15
# !@Author : DongHan Yang
# !@File   : templates.py

from template.cpmn import *


class MCT:
    def __init__(self, key, value, targ):
        self.key = key
        self.value = value
        self.targ = targ
        self.cost = self.calCost(key, value)

    # 有问题
    def calCost(self, key, value):
        c = bin(key).count('1')
        costNot = c - bin(value).count('1')
        return costNot * 2 + 12 * (c + 1) - 34


class templateMatch:
    def __init__(self, MCT1, MCT2):
        key1 = MCT1.key
        key2 = MCT2.key
        self.MCT1 = MCT1 if bin(key1).count('1') > bin(key2).count('1') else MCT2
        self.MCT2 = MCT2 if bin(key1).count('1') <= bin(key2).count('1') else MCT1
        self.key1 = MCT1.key
        self.key2 = MCT2.key
        self.value1 = MCT1.value
        self.value2 = MCT2.value
        self.preCost = MCT1.cost + MCT2.cost
        self.finCost = 0
        self.reduceCost = 0

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
            g1 = MCT(big, newValue, -1)
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
            newValue1 = removeKeyValue(newKey, small, y1)
            # putGates(newKey, newValue1, gates)
            g1 = MCT(big, newValue, -1)
            g2 = MCT(newKey, newValue1, -1)
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
            newM = M if bin(N).count('1') == 1 else N
            newN = N if newM == M else M
            newKey1 = key1 if newM == M else key2
            newKey2 = key2 if newKey1 == key1 else key1
            x1 = value1 if newKey1 == key1 else value2
            y1 = value2 if x1 == value1 else value1
            # 从里面去除
            # removeGates(newKey1, x1, gates)  # g1
            # removeGates(newKey2, y1, gates)  # g2
            # 结构块放入结果
            newValueM = removeKeyValue(newM, newKey1, x1)
            toffi = MCT(newM, newValueM, newN)
            g3 = MCT(newKey2, y1, -1)
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
            newValue2 = removeKeyValue(P, key2, value2)
            newKey2 = key2 ^ P
            g4 = MCT(newKey2, newValue2, -1)
            # toffi
            PM = P ^ M
            pmValue = removeKeyValue(PM, key1, value1)  # pm,pmvalue
            toffi = MCT(PM, pmValue, N)
            # cnot
            nValue = removeKeyValue(N, key2, value2)  # n,nvalue
            cnot = MCT(PM, nValue, M)
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
        global inputN
        C, P, M, N = getCpmn(key1, value1, key2, value2)
        allKeys = C ^ P ^ M ^ N
        if bin(P).count('1') == 1 and bin(allKeys).count('1') < inputN:  # 有其他条件
            unUsed = ((1 << inputN) - 1) ^ allKeys
            u = unUsed & (-unUsed)  # target
            PM = P ^ M
            PN = P ^ N
            pmValue1 = removeKeyValue(PM, key1, value1)
            g1 = MCT(PM, pmValue1, u)
            pmValue2 = removeKeyValue(PN, key2, value2)
            g3 = MCT(PN, pmValue2, u)
            Cu = C ^ u
            cuValue = insertKeyValue(Cu, key1, value1)
            g2 = MCT(Cu, cuValue, -1)

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
            P0 = P & (P - 1)
            pValue = removeKeyValue(P0, key1, value1)
            print(f'pValue一位:', pValue)
            newKey1 = key1 if pValue == 1 else key2  # 错误
            newKey2 = key2 if key1 == newKey1 else key1
            newValue1 = value1 if newKey1 == key1 else value2
            newValue2 = value2 if value1 == newValue1 else value1
            # P最高位置为0
            #  newKey1,value3
            P3 = P ^ P0
            value3 = changeValue(P3, newKey1, newValue1)
            g3 = MCT(newKey1, value3, -1)
            # newKey2,newValue2
            conutP3 = P3
            cnotList = []
            while conutP3:
                pLow = conutP3 & (conutP3 - 1)
                g = MCT(P0, 1, pLow)
                conutP3 &= (-conutP3)
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
            p3 = templateMatch(g3, self.MCT2)
            opt = p3.template6Optimize()
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
            rValue = removeKeyValue(C, key1, value1)
            ret = MCT(C, rValue, -1)
            self.finCost = ret.cost
            self.reduceCost = self.preCost - self.finCost
            return MCT(C, rValue, -1)
        elif bin(M).count('1') + bin(N).count('1') == 1:
            return self.template2()
        elif bin(M).count('1') == 1 and bin(N).count('1') == 1:
            return self.template4()
        elif bin(M).count('1') == 1 and bin(N).count('1') == 1:
            return self.template5()

    def optimize(self):
        key1 = self.key1
        value1 = self.value1
        key2 = self.key2
        value2 = self.value2
        C, P, M, N = getCpmn(key1, value1, key2, value2)
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
                and bin(P).count('1') == 1 and bin(allKeys).count('1') < inputN:
            return self.template5()
        elif type == 6 and bin(M).count('1') == 1 and bin(N).count('1') == 1:
            return self.template6()

    def setCost(self, gatesList):
        sumCost = 0
        for g in gatesList:
            sumCost += g.cost
        self.finCost = sumCost
        self.reduceCost = self.preCost - self.finCost


# gates放入新值
def putGates(newKey, newValue, gates):
    if newKey in gates:  # 去重
        if newValue not in gates[newKey]:
            gates[newKey].append(newValue)
        else:
            gates[newKey].remove(newValue)
    else:
        gates[newKey] = [newValue]


# gates改变值
def changeGates(newKey, oldValue, newValue, gates):
    if newValue in gates[newKey]:
        gates[newKey].remove(newValue)
    else:
        gates[newKey].remove(oldValue)
        gates[newKey].append(newValue)


# gates删除值
def removeGates(Key, Value, gates):
    gates[Key].remove(Value)
    if len(gates[Key]) == 0:
        del gates[Key]
