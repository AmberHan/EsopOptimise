# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/3/2 12:03
# !@Author : DongHan Yang
# !@File   : plaTotfc.py
import os.path


class pla:
    def __init__(self, name):
        self.name = name
        self.path = os.path.dirname(os.path.abspath(__file__)) + os.path.sep
        self.top = ""
        self.c = ""
        self.ends = ""
        self.pControl = []

    def readPla(self):
        self.getTop()
        self.getGates()

    def getGates(self):
        fileName = self.path + self.name + '.txt'
        with open(fileName, 'r') as f:
            c = f.readline()
            while c.count('begin') != 1:
                c = f.readline()
            c = f.readline()
            strGates = ""
            while c.count('end') != 1:
                gateStr = c.strip('\n')
                vargates = gateStr.split(' ')
                if vargates[0] == 't1':
                    if vargates[1] not in self.pControl:
                        self.pControl.append(vargates[1])
                    else:
                        self.pControl.remove(vargates[1])
                else:
                    strGates += (vargates[0] + " ")
                    strGates += self.getXstr(vargates[1:])
                    # strGates += ",".join(vargates[1:])
                    strGates += "\n"
                c = f.readline()
        strGates += 'END'
        self.ends = strGates
        f.close()

    def getXstr(self, xList):
        retXList = []
        for x in xList:
            if x not in self.pControl:
                retXList.append(x)
            else:
                y = x + "'"
                retXList.append(y)
        return ",".join(retXList)

    # 存放头部信息，以及初始化f和c
    def getTop(self):
        fileName = self.path + self.name + '.txt'
        with open(fileName, 'r') as f:
            topStr = ""
            c = f.readline()
            while c.count('begin') != 1:
                if c[0] == '#':  # 注释抛弃
                    c = f.readline()
                    continue
                c = c.strip('\n')
                varfx = c.split(' ')
                if c.count('.variables'):
                    topStr += (".v " + self.getfx(varfx, 'v') + '\n')
                elif c.count('.inputs'):
                    topStr += (".i " + self.getfx(varfx, 'i') + '\n')
                elif c.count('.outputs'):
                    topStr += (".o " + self.getfx(varfx, 'o') + '\n')
                elif c.count('.constants'):
                    topStr += (".c " + self.c + '\n')
                c = f.readline()
        f.close()
        self.top = topStr + "BEGIN\n"

    def getfx(self, strList, c):
        retList = []
        ret0 = []
        for s in strList:
            if c == 'v' and (s.count('f') or s.count('x')):
                retList.append(s)
            elif c == 'i':
                if s.count('x'):
                    retList.append(s)
                elif s.count('0'):
                    ret0.append(s)
            elif c == 'o' and s.count('f'):
                retList.append(s)
        if len(ret0) != 0:
            self.c = ",".join(ret0)
        return ",".join(retList)

    def writeTfc(self):
        fileName = self.path + self.name + '.tfc'
        with open(fileName, 'w') as f:
            f.write(self.top + self.ends)
        f.close()


def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            names = os.path.splitext(file)
            if names[1] == '.txt':  # 想要保存的文件格式
                L.append(names[0])
    return L


if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    txtName = file_name(path)
    print(txtName)
    for strl in txtName:
        print(strl)
        t = pla(strl)
        t.readPla()
        t.writeTfc()
