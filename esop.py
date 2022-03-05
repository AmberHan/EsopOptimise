# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/2/27 23:12
# !@Author : DongHan Yang
# !@File   : esop.py
from tfcReadWrite import *
from Match import *


# from benchmarks.readname import *


class esop:
    # key对应fx, value对应门
    # totalGates: {1:[(key,value)],10:[(key,value),(key1,value1)]}
    def __init__(self, totalGates, inLineNum, outLineNum):
        self.totalGates = totalGates
        self.inLineNum = inLineNum
        self.outLineNum = outLineNum
        self.lines2 = self.getLines()  # 所有2的组合
        self.fxGates = {}  # xg
        self.table1 = self.step1()  # 表1
        # self.getMaxShare()  # 错误
        self.table2, self.table2Cost, self.table2CostKey = self.step2()  # 表2
        self.maxCost = self.getMaxCost()  # 得到最大代价列表
        # 返回fxGates:
        # {0001:[(key,value),(key,value),(key,value)],0011:[(key,value),(key,value),(key,value)]}
        self.getGates()  # 存放其他门

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
        dp1 = [[[0] * m for _ in range(n)] for _ in range(m)]  # 记录最大代价路径
        # 初始条件
        for j in range(n):
            dp[0][j] = table2Cost[table2CostKey[j]]
            dp1[0][j][0] = table2CostKey[j]
        for i in range(1, m):
            for j in range(n):
                dp1[i][j] = copy.deepcopy(dp1[i - 1][j])  # xg
                nowKey = nowCostKey[j]  # 获取上一行取值情况
                dp[i][j] = copy.deepcopy(dp[i - 1][j])
                for costKey in table2CostKey:
                    # if costKey & nowKey == 0 and dp[i][j] <= dp[i - 1][j] + table2Cost[costKey]:
                    #     dp[i][j] = dp[i - 1][j] + table2Cost[costKey]
                    #     dp1[i][j] = copy.deepcopy(dp1[i - 1][j])
                    #     dp1[i][j][i] = costKey
                    if costKey & nowKey == 0 and dp[i][j] < dp[i - 1][j] + table2Cost[costKey]:
                        dp[i][j] = dp[i - 1][j] + table2Cost[costKey]
                        dp1[i][j][i] = costKey  # fx 对应的
                nowCostKey[j] = nowKey ^ dp1[i][j][i]  # 持续j次维护当前行的取值情况
        # 找到二维表最后一行最大值，记录列号
        # maxCost, col = nowCostKey[0], 0
        #         # for j in range(1, n):
        #         #     if maxCost < nowCostKey[j]:
        #         #         maxCost = nowCostKey[j]
        #         #         col = j
        #         #     elif maxCost == nowCostKey[j] and set(dp1[m - 1][j]) != set(dp1[m - 1][col]):
        #         #         print("存在多解")
        maxCost, col = 0, 0
        for mcIndex in range(len(dp[m - 1])):
            if dp[m - 1][mcIndex] > maxCost:
                maxCost, col = dp[m - 1][mcIndex], mcIndex
        maxCost1 = dp1[m - 1][col]  # 最大代价路径
        sameNum = 0
        for index in range(len(dp[m - 1])):
            if dp[m - 1][index] == maxCost and set(maxCost1) != set(dp1[m - 1][index]):
                sameNum += 1
        print(f"存在{sameNum}解")
        return maxCost1

    # 维护表1，进行选择门
    # fxGates  {0001:[(key,value),(key,value),(key,value)],0011:[(key,value),(key,value),(key,value)]}
    # 1个1 代表f1,2个1表示两个门相连
    # 得到可以优化的组合
    def getGates(self):
        # fxGates = self.fxGates
        table2 = self.table2
        for lines2 in self.maxCost:
            if lines2 == 0:
                break
            for gTup in table2[lines2]:  # table2[lines2]表示一组的门，可以后续优化，lines2两个门
                if self.table1[gTup] & lines2 != lines2:
                    print("错误")
                self.table1[gTup] ^= lines2  # 维护表1，进行选择门，表示已经选择
            self.fxGates[lines2] = table2[lines2]
        for i in range(self.outLineNum):
            ls = 1 << i
            # fxGate = {l: []}
            for gateTup, f in self.table1.items():
                if ls & f == ls:
                    self.table1[gateTup] ^= ls
                    # fxGate[l].append(gateTup)
                    self.pushTable2(ls, gateTup, self.fxGates)
            # fxGates.append(fxGate)
        # print(fxGates)
        # return fxGates

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

    # 表1：{(key,value):0011，(key1,value1):0011}
    # 找到最大代价的共享块3个1，4个1...，找到最大的共享
    # 其中需要维护表1，消去1使用的1，
    # 输出{f123:{(key,value,0),(key,value,0)}}，可能多个1，根据key获取代价
    def getMaxShare(self):
        outNum = self.outLineNum
        allCost = 0
        chooseFx = 0
        for i in range(3, outNum + 1):
            onesList = self.calOneList(i)  # 获取所有的情况
            for ones in onesList:
                sumCost = 0
                for gateSet, fxs in self.table1.items():
                    if fxs & ones == ones:
                        sumCost += self.calCost(gateSet)
                thisAllCost = sumCost * (i - 1)
                if thisAllCost > allCost:
                    allCost = thisAllCost
                    chooseFx = ones
        if chooseFx != 0:
            for gateSet, fxs in self.table1.items():
                if fxs & chooseFx == chooseFx:
                    self.table1[gateSet] ^= chooseFx  # 维护表1
                    self.pushTable2(chooseFx, gateSet, self.fxGates)  # 存放最大匹配的结果
            print(f"第一步优化门{self.fxGates}")

    # 生成多个1所有情况；>2
    def calOneList(self, oneNums):
        oneList = []
        numss = (1 << self.outLineNum) - 1
        for i in range(numss + 1):
            if bin(i).count('1') == oneNums:
                oneList.append(i)
        return oneList

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
                vc = 12 * (cNums + 1) - 34
        elif n - cNums >= 1:
            if cNums <= 9:
                vc = cost1[cNums]
            else:
                vc = 24 * (cNums + 1) - 88
        else:
            if cNums <= 9:
                vc = cost0[cNums]
            else:
                vc = 2 ** (cNums + 1) - 3
        if gatesTup[1] == 0:
            vc += 1
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
    # totalGates = {0b1000: [(0b110, 0), (0b010, 1), (0b001, 1)], 0b0100: [(0b110, 3), (0b010, 1)],
    #               0b0010: [(0b001, 1), (0b011, 3)], 0b0001: [(0b001, 1)]}
    path = os.path.dirname(os.path.abspath(__file__))
    allBenchmarks = file_name(path + "\\benchmarks")
    # print(allBenchmarks)
    mmp = ['5xp', '5xp1_194', 'alu2_199', 'apex4_202', 'apla_203', 'clip_206', 'cm150a_210', 'cordic_218', 'cu_219',
           'dc1_221', 'dc2_222', 'dec', 'decod_217', 'dist_223', 'f51m_233', 'frg1_234', 'in0_235', 'in2_236',
           'inc_237',
           'life_238', 'table3_264', 'z4ml_269', 'z4_268', 'alu2_199', 'in2_236',
           '  ',
           'z4ml_269', 'z4_268']

    allBenchmarks = ["cm150a_210"]
    for benchmarkName in allBenchmarks:
        print(benchmarkName)
        t = tfc(benchmarkName)
        t.readTfc()
        totalGates, inLine, outLine = t.retGatesDict, t.inNum, t.outNum
        print(totalGates)
        # 阶段0 统计门的最大代价共享
        # 阶段1输出：{f1f2:[(key,value),()], f1:[(),()], f2:[(),()]}
        if outLine > 1:
            tt = esop(totalGates, inLine, outLine)
            totalGates = tt.fxGates
            print(totalGates)  # 打印阶段1结果
            t.writeTxt(totalGates, 1)  # 阶段1写入文件

        # 阶段2：处理 [(key,value,0),(key,value,1)], 进行模板匹配
        newGatesDict = {}
        for fKey, gatesTupList in totalGates.items():
            if len(gatesTupList) == 1:
                newGatesDict[fKey] = gatesTupList
            else:
                mt = Match(fKey, gatesTupList, inLine)
                newGatesDict[fKey] = mt.solveRetGatesList
        t.writeTxt(newGatesDict, 2)
        # 阶段2输出：{f1f2:[(key,value,-1),(key,value,u)], f1:[(),()], f2:[(),()]}
        # 根据.v获取 in, outnum;建立索引
        # 根据key得知t4,根据key获取X0，X1；根据value得知+-；最后一个根据-1为key，正数为对应key
