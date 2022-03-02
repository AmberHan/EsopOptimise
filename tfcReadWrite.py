# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/2/28 17:58
# !@Author : DongHan Yang
# !@File   : tfcReadWrite.py
import os.path
import math


class tfc:
    def __init__(self, name):
        self.name = name + ".tfc"
        self.path = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "benchmarks\\"
        self.fs, self.cs, self.mct, self.inNum, self.outNum = [], [], [], 0, 0
        self.retGatesDict = {}
        self.top = ""

    def readTfc(self):
        self.getTop()
        self.getGates()

    # 存放门{f1:[(),(),()],f2:[(),(),()]}
    def getGates(self):
        fileName = self.path + self.name
        with open(fileName, 'r') as f:
            c = f.readline()
            while c.count('BEGIN') != 1:
                c = f.readline()
            c = f.readline()
            while c.count('END') != 1:
                gateStr = c.strip('\n')
                ft, key, value, type = self.solveGateStr(gateStr)
                self.putGates(ft, key, value, type)
                c = f.readline()
        f.close()

    # 存放门
    def putGates(self, ft, key, value, type):
        if ft not in self.retGatesDict:
            self.retGatesDict[ft] = [(key, value, type)]
        else:
            self.retGatesDict[ft].append((key, value, type))

    # 处理一行门信息，得到key,value
    def solveGateStr(self, gateStr):
        gateStrList = gateStr.split(' ')
        mct = gateStrList[0]
        controlLine = gateStrList[1].split(',')
        if mct.count(str(len(controlLine))) != 1:
            print("false")
        j, m, key, value = 0, 0, 0, 0
        for x in self.cs:
            if m < len(controlLine) - 1 and controlLine[m].count(x):
                key ^= (1 << j)
                if controlLine[m].count("'") != 1:
                    value ^= (1 << m)
                m += 1
            j += 1
        type, ft = 0, 0
        if controlLine[-1] in self.fs:
            ft = (1 << self.fs.index(controlLine[-1]))
        else:
            type = (1 << self.cs.index(controlLine[-1]))
        return ft, key, value, type

    # 存放头部信息，以及初始化f和c
    def getTop(self):
        fileName = self.path + self.name
        with open(fileName, 'r') as f:
            topStr = ""
            c = f.readline()
            while c.count('BEGIN') != 1:
                if c[0] == '#':  # 注释抛弃
                    c = f.readline()
                    continue
                topStr += c
                if c.count('.v'):
                    c = c.strip('\n')
                    strfx = c.split(' ')
                    fx = strfx[1].split(',')
                    self.savefx(fx)
                c = f.readline()
        f.close()
        self.top = topStr

    # 存储f、x线以及mct
    def savefx(self, fxList):
        fs = []
        cs = []
        for i in range(len(fxList) - 1, -1, -1):
            if fxList[i].count('f'):
                fs.append(fxList[i])
            elif fxList[i].count('x'):
                cs.append(fxList[i])
        self.fs, self.cs = fs, cs
        self.inNum, self.outNum = len(cs), len(fs)
        for i in range(self.inNum + 1):
            self.mct.append("t" + str(i + 1))

    # gates: {512: [(18, 3, 0), (29, 15, 0)],...}
    def writeTxt(self, gates, step):
        fileName = self.path + "new" + str(step) + self.name
        with open(fileName, 'w') as f:
            f.write(self.top)
            f.write("BEGIN\n")
            for fKey, gatesList in gates.items():
                for gateTup in gatesList:
                    key, value, ft = gateTup[0], gateTup[1], gateTup[2]
                    gateStr = self.getGateStr(fKey, key, value, ft)
                    f.write(gateStr)
                if bin(fKey).count('1') == 2:
                    cKey = fKey & (-fKey)
                    fcIndex = int(math.log2(cKey))
                    notC = self.fs[fcIndex]
                    fKey &= (fKey - 1)
                    ftIndex = int(math.log2(fKey))
                    notT = self.fs[ftIndex]
                    cnotStr = "t2 " + notC + "," + notT + "\n"
                    f.write(cnotStr)
                elif bin(fKey).count('1') > 2:
                    print("error")
            f.write("END")
        f.close()

    # 获取门序列
    def getGateStr(self, fKey, key, value, ft):
        fIndex = bin(key).count('1')
        gateStr = self.mct[fIndex] + ' '
        if ft == 0:
            fKey &= (-fKey)  # 获取最低位1
            fcIndex = int(math.log2(fKey))
            ftStr = self.fs[fcIndex]
        else:
            fcIndex = int(math.log2(ft))
            ftStr = self.cs[fcIndex]
        cStr = self.getControlGate(key, value)
        if cStr == '':
            retStr = gateStr + ftStr + "\n"
        else:
            retStr = gateStr + cStr + "," + ftStr + "\n"
        return retStr

    # 根据key,value,返回x0,x1'
    def getControlGate(self, key, value):
        index = 0
        cList = []
        while key:
            if key % 2 == 1:
                cList.append(self.cs[index])
                if value % 2 == 0:
                    cList[-1] += "'"
                value >>= 1
            index += 1
            key >>= 1
        return ",".join(cList)


if __name__ == '__main__':
    t = tfc("dec")
    t.readTfc()
    g = t.retGatesDict
    print(t.retGatesDict)
    t.writeTxt(g,0)
