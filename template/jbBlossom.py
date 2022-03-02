# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/1/11 15:24
# !@Author : DongHan Yang
# !@File   : jbBlossom.py

from sys import stdin
from collections import deque


class Node:
    def __init__(self, no):
        self.no = no
        self.mate = None
        self.neibr = []
        self.blossom = None
        self.ce_near = None
        self.ce_far = None
        self.par = None
        self.odd = -1
        self.lca_flg = -1

    def reset(self):
        self.blossom = self
        self.odd = -1
        self.lca_flg = -1
        self.par = None

    def match(self, other):
        self.mate = other
        other.mate = self

    def broot(self):
        if self.blossom != self:
            self.blossom = self.blossom.broot()
        return self.blossom

    pass


def lca(x, y, rt):
    while x != y and x.lca_flg != 2 and y.lca_flg != 1:
        x.lca_flg, y.lca_flg = 1, 2
        if x is not rt:
            x = x.par.broot()
        if y is not rt:
            y = y.par.broot()
    if y.lca_flg == 1:
        p, q = y, x
    else:
        p, q = x, y
    x = p
    while x is not q:
        x.lca_flg = -1
        x = x.par.broot()
    x.lca_flg = -1
    return p


def contract(blossom, near, far, q):
    x = near.broot()
    while x is not blossom:
        x.blossom = blossom
        if x.odd == 1:
            x.ce_near = near
            x.ce_far = far
            q.append(x)
        x = x.par.broot()


def flip(rt, x):
    if x is not rt:
        if x.odd == 0:
            flip(rt, x.par.par)
            x.par.par.match(x.par)
        else:
            flip(x.mate, x.ce_near)
            flip(rt, x.ce_far)
            x.ce_near.match(x.ce_far)


def bfs(g, rt):
    for x in g:
        x.reset()
    rt.odd = 0
    q = deque([rt])
    while q:
        x = q.popleft()
        xblos = x.broot()
        for y in x.neibr:
            yblos = y.broot()
            if (y.mate is y) or (xblos is yblos):
                continue
            if y.odd == -1:
                if y.mate is None:
                    flip(rt, x)
                    x.match(y)
                    return True
                else:
                    y.par = x
                    y.odd = 1
                    y.mate.par = y
                    y.mate.odd = 0
                    q.append(y.mate)
            elif yblos.odd == 0:
                blossom = lca(xblos, yblos, rt)
                contract(blossom, x, y, q)
                contract(blossom, y, x, q)
    return False


def max_match(n, e):
    g = [Node(i) for i in range(n)]
    ans = 0

    for x, y in e:
        g[x].neibr.append(g[y])
        g[y].neibr.append(g[x])
        if (g[x].mate is None) and (g[y].mate is None):
            g[x].match(g[y])
            ans += 1

    for x in g:
        if x.mate is None:
            if bfs(g, x):
                ans += 1
            else:
                x.mate = x
    return ans, g


# 输入一堆数，以及异或目标;输出二位匹配数组
def xor_num(lists, num):
    n = len(lists)
    o_rets = list()
    ret_set = set()
    for i in range(n):
        for j in range(i + 1, n):
            if bin(lists[i] ^ lists[j]).count('1') == num:
                o_rets.append([lists[i], lists[j]])
                ret_set.add(lists[i])
                ret_set.add(lists[j])
    # ret_list所有节点，n_rets映射返回节点
    ret_list = list(ret_set)
    n_rets = list()
    for pairs in o_rets:
        n_rets.append([ret_list.index(pairs[0]), ret_list.index(pairs[1])])
    return ret_list, n_rets


def jb_blossom(new_gates):
    for key, value in new_gates.items():
        new_value = []
        for i in range(1, 11):
            # node为节点本身，e为node索引的边关系
            node, e = xor_num(value, i)
            # 所有异或为i的进行搭配邻接
            n_v = blossom(node, e)
            new_value.extend(n_v)
            # 余下没有匹配的
            value = list(set(value) - set(new_value))

            if len(value) == 1:
                new_value.extend(value)
                break
            # elif len(value) == 0:
            #     print(f"当前最大异或：", i)
            #     break
            # if i >= 2:
            #     print(f"当前余下：", len(value))
        if set(new_gates[key]) == set(new_value):
            # print("same")
            pass
        else:
            print("different")
            print(new_gates[key])
            print(new_value)
        new_gates[key] = new_value


def blossom(node, e):
    n = len(node)
    ans, g = max_match(n, e)
    rets = list()
    # stdout.write(str(ans) + "\n")
    for index, x in enumerate(g):
        if (x.mate is not x) and (x.mate is not None) and node[x.mate.no] not in rets:
            rets.append(node[index])
            rets.append(node[x.mate.no])
            # stdout.write(str(x.mate.no + 1) + " ")
    #     else:
    #         stdout.write("0 ")
    # stdout.write("\n")
    return rets


if __name__ == "__main__":
    [n, m] = map(int, stdin.readline().split(" "))
    e = [list(map(lambda v: int(v) - 1, stdin.readline().split(" "))) for _ in range(m)]
    blossom(n, e)
