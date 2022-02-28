# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/2/27 23:12
# !@Author : DongHan Yang
# !@File   : esop.py
import copy


class esop:
    # key对应fx, value对应门
    # totalGates: {1:[(key,value)],10:[(key,value),(key1,value1)]}
    def __init__(self, totalGates, inLineNum, outLineNum):
        self.totalGates = totalGates
        self.inLineNum = inLineNum
        self.outLineNum = outLineNum
        self.lines2 = self.getLines()  # 所有2的组合
        self.table1 = self.step1()  # 表1
        self.table2, self.table2Cost, self.table2CostKey = self.step2()  # 表2
        self.maxCost = self.getMaxCost()  # 得到最大代价列表
        # 返回fxGates:
        # {0001:[(key,value),(key,value),(key,value)],0011:[(key,value),(key,value),(key,value)]}
        self.fxGates = self.getGates()

        # 返回最大代价的匹配结果[0011,1100]

    # table2Cost: {0011: totalCost, 0101: totalCost1}
    # table2CostKey: [0011,1100]
    def getMaxCost(self):
        table2Cost = self.table2Cost  # 读取代价
        table2CostKey = self.table2CostKey
        nowCostKey = copy.deepcopy(table2CostKey)  # 记录每次迭代当前格子的 0011情况
        m = self.outLineNum // 2
        n = len(table2CostKey)
        dp = [[0] * n for _ in range(m)]
        dp1 = [[[0] * m] * n for _ in range(m)]  # 记录最大代价路径
        # 初始条件
        for j in range(n):
            dp[0][j] = table2Cost[table2CostKey[j]]
            dp1[0][j][0] = table2CostKey[j]
        for i in range(1, m):
            for j in range(n):
                nowKey = nowCostKey[j]  # 获取上一行取值情况
                for costKey in table2CostKey:
                    if costKey & nowKey == 0 and dp[i][j] < dp[i - 1][j] + table2Cost[costKey]:
                        dp[i][j] = dp[i - 1][j] + table2Cost[costKey]
                        dp1[i][j] = dp1[i - 1][j]
                        dp1[i][j][i] = costKey
                nowCostKey[j] = nowKey ^ dp1[i][j][i]  # 持续j次维护当前行的取值情况
        # 找到二维表最后一行最大值，记录列号
        maxCost, col = nowCostKey[0], 0
        for j in range(1, n):
            if maxCost < nowCostKey[j]:
                maxCost = nowCostKey[j]
                col = j
            elif maxCost == nowCostKey[j] and set(dp1[m - 1][j]) != set(dp1[m - 1][col]):
                print("存在多解")
        maxCost = dp1[m - 1][col]
        return maxCost

    # 维护表1，进行选择门
    # fxGates  {0001:[(key,value),(key,value),(key,value)],0011:[(key,value),(key,value),(key,value)]}
    # 1个1 代表f1,2个1表示两个门相连
    # 得到可以优化的组合
    def getGates(self):
        fxGates = {}
        table2 = self.table2
        for lines2 in self.maxCost:
            for gTup in table2[lines2]:  # table2[lines2]表示一组的门，可以后续优化，lines2两个门
                self.table1[gTup] ^= lines2  # 维护表1，进行选择门，表示已经选择
            fxGates[lines2] = table2[lines2]
        for i in range(self.outLineNum):
            l = 1 << i
            fxGate = {l: []}
            for gateTup, f in self.table1.items():
                if l & f == l:
                    self.table1[gateTup] ^= l
                    # fxGate[l].append(gateTup)
                    self.pushTable2(l, gateTup, fxGates)
            # fxGates.append(fxGate)
        print(fxGates)
        return fxGates

    # 步骤1：维护字典表1
    # {(key,value):0011，(key1,value1):0011}
    # 表示门key,value，在f1和f2中存在
    def step1(self):
        table1 = {}
        # for f, gates in self.totalGates.items():
        # for key, value in gates.items():
        #     table1[(key, value)] ^= f if (key, value) in table1 else 0
        for f, gatesTupList in self.totalGates.items():
            for gatesTup in gatesTupList:
                table1[gatesTup] = f ^ table1[gatesTup] if gatesTup in table1 else f
        return table1

    # 步骤2，生成字典表2
    # table2:     {0011:[(key,value),(key1,value1)],0101:[(key,value),(key1,value1)]}
    # table2CostKey: [0011,0101]
    # table2Cost: {0011:totalCost,0101:totalCost1}
    # 2根线情况下，包含的门情况，需要维护
    def step2(self):
        table2 = {}
        table2Cost = {}
        table2CostKey = []
        for line2 in self.lines2:
            for gatesTup, f in self.table1.items():
                if f & line2 == line2:
                    self.pushTable2(line2, gatesTup, table2)
                    self.calTable2(line2, gatesTup, table2Cost)
        for key, _ in table2Cost.items():
            table2CostKey.append(key)
        return table2, table2Cost, table2CostKey

    def pushTable2(self, mapKey, tup, table):
        if mapKey not in table:
            table[mapKey] = [tup]
        else:
            table[mapKey].append(tup)

    def calTable2(self, line2, gatesTup, tableCost):
        if line2 not in tableCost:
            tableCost[line2] = self.calCost(gatesTup)
        else:
            tableCost[line2] += self.calCost(gatesTup)

    # 计算单个门代价
    def calCost(self, gatesTup):
        cost0 = [1, 1, 5, 13, 29, 61, 125, 253, 509, 1021]
        cost1 = [1, 1, 5, 13, 29, 52, 80, 100, 128, 152]
        cost2 = [1, 1, 5, 13, 26, 38, 50, 62, 74, 86]
        cNums = bin(gatesTup[0]).count('1')
        n = self.inLineNum + self.outLineNum
        if n - cNums >= cNums - 2:
            if cNums <= 9:
                vc = cost2[cNums]
            else:
                vc = 2 ** (cNums + 1) - 3
        elif n - cNums >= 1:
            if cNums <= 9:
                vc = cost1[cNums]
            else:
                vc = 24 * (cNums + 1) - 88
        else:
            if cNums <= 9:
                vc = cost0[cNums]
            else:
                vc = 12 * (cNums + 1) - 34
        if gatesTup[1] == 0:
            vc += 2
        return vc

    # 所有2个1的情况
    def getLines(self):
        lines2 = []
        n = self.outLineNum
        for i in range(n):
            l = 1 << i
            for j in range(i + 1, n):
                r = 1 << j
                line2 = l ^ r
                lines2.append(line2)
        return lines2


if __name__ == '__main__':
    # {f1:[(),(),()],f2:[(),(),()]}，inline,outline
    totalGates = {0b1000: [(0b110, 0), (0b010, 1), (0b001, 1)], 0b0100: [(0b110, 3), (0b010, 1)],
                  0b0010: [(0b001, 1), (0b011, 3)], 0b0001: [(0b001, 1)]}
    # 阶段1输出：{f1f2:[(),()], f1:[(),()], f2:[(),()]}
    t = esop(totalGates, 3, 4)
    # 阶段2：处理 [(),()], 进行模板匹配
    pass
