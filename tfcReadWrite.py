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
        # self.path1 = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "benchmarks\\3\\"
        self.path = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "benchmarks\\3\\"
        self.fs, self.cs, self.mct, self.inNum, self.outNum = [], [], [], 0, 0
        self.retGatesDict = {}
        self.top = ""
        self.fnot = 0

    def readTfc(self):
        self.getTop()
        self.getGates()

    # 存放门{f1:[(),(),()],f2:[(),(),()]}
    def getGates(self):
        fileName = self.path + "tfc\\" + self.name
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
        fileName = self.path + "tfc\\" + self.name
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
    def writeTxt(self, gates, step, unused):
        fileName = self.path + "testResult\\" + "phase" + str(step) + "_" + self.name
        try:
            os.remove(fileName)
        except:
            print("移除失败")
        with open(fileName, 'w') as f:
            f.write(self.top)
            f.write("BEGIN\n")
            for fKey, gatesList in gates.items():
                for gateTup in gatesList:
                    key, value, ft = gateTup[0], gateTup[1], gateTup[2]
                    if bin(key) == 1 and value == 0:  # cnot 取反
                        value = 1
                        self.fnot ^= fKey
                    gateStr = self.getGateStr(fKey, key, value, ft, unused)
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
                    countKey = fKey
                    while bin(countKey).count('1') > 1:
                        cKey = countKey & (-countKey)  # 获取c
                        fcIndex = int(math.log2(cKey))
                        notC = self.fs[fcIndex]
                        countKey &= (countKey - 1)  # 除去
                        fKey = countKey & (-countKey)  # 获取t
                        ftIndex = int(math.log2(fKey))
                        notT = self.fs[ftIndex]
                        cnotStr = "t2 " + notC + "," + notT + "\n"
                        f.write(cnotStr)
            while self.fnot:
                low = self.fnot & (self.fnot - 1)
                flow = int(math.log2(low))
                notStr = "t1 " + self.fs[flow] + notT + "\n"
                f.write(notStr)
                self.fnot &= (-self.fnot)
            f.write("END")
        f.close()

    # 获取门序列
    # def getGateStr(self, fKey, key, value, ft):
    #     fIndex = bin(key).count('1')
    #     gateStr = self.mct[fIndex] + ' '
    #     ckey = fKey & (-fKey)
    #     if ft == 0:
    #         # fKey &= (-fKey)  # 获取最低位1
    #         fcIndex = int(math.log2(ckey))
    #         ftStr = self.fs[fcIndex]
    #     else:
    #         fcIndex = int(math.log2(ft))
    #         ftStr = self.cs[fcIndex]
    #
    #     cStr = self.getControlGate(key, value)
    #     if cStr == '':
    #         retStr = gateStr + ftStr + "\n"
    #     else:
    #         retStr = gateStr + cStr + "," + ftStr + "\n"
    #     return retStr
    #

    # 使用受控线
    def getGateStr(self, fKey, key, value, ft, unused):
        fIndex = bin(key).count('1')
        gateStr = self.mct[fIndex] + ' '
        ckey = fKey & (-fKey)
        if ft > 0:
            fcIndex = int(math.log2(ft))
            ftStr = self.cs[fcIndex]
        elif ft == -1:
            # 模板5的g1
            common = ckey & unused
            usedf = common ^ unused
            if usedf != 0:
                usedf &= (usedf - 1)
                fcIndex = int(math.log2(usedf))
                ftStr = self.fs[fcIndex]
        else:  # if ft == 0:为0和-2时候，表示受控点在f上
            # fKey &= (-fKey)  # 获取最低位1
            fcIndex = int(math.log2(ckey))
            ftStr = self.fs[fcIndex]
        cStr = self.getControlGate(key, value)
        if cStr == '':
            retStr = gateStr + ftStr + "\n"
        else:
            retStr = gateStr + cStr + "," + ftStr + "\n"
        if ft == -2:  # 需要新增一个控制点 u,修改t
            retlst = retStr.split(' ')
            tn = int(retlst[0][1]) + 1  # 修改t
            common = ckey & unused
            usedf = common ^ unused
            if usedf != 0:
                usedf &= (usedf - 1)
                fccIndex = int(math.log2(usedf))
                fttStr = self.fs[fccIndex]
                retStr = "t" + str(tn) + " " + fttStr + "," + retlst[1]
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


def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            names = os.path.splitext(file)
            if names[1] == '.tfc':  # 想要保存的文件格式
                L.append(names[0])
    return L


if __name__ == '__main__':
    t = tfc("dec")
    t.readTfc()
    g = t.retGatesDict
    print(t.retGatesDict)
    t.writeTxt(g, 0, 0)
