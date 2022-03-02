# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/1/12 22:03
# !@Author : DongHan Yang
# !@File   : mode2.py
import copy
# 按照模式2进行修改，每次删除一个控制点
def mode2(gates):
    # n_gates = dict(sorted(gates.items(), key=lambda x: -bin(x[0]).count("1")))
    # print(n_gates)
    n_gates = copy.deepcopy(gates)
    # 初始化，集中所有的key
    keys = []
    for key, _ in n_gates.items():
        keys.append(key)
    while wh_key(keys, n_gates):
        pass
        # wh_key(keys, n_gates)
    return n_gates


def wh_key(keys, n_gates):
    n = len(keys)
    for i in range(n):
        for j in range(i + 1, n):
            if match(keys[i], keys[j], keys, n_gates):
                return True
    return False


# 求last_index是key中第几个1，对应x1中第几值要删除
def get_key(big, last_index):
    l_index = bin((last_index - 1) & big).count("1")
    return l_index


# 如01(1)010, 010 对应倒数第2个1取反 -> 01(0)010
def get_key2(key, index):
    c_key = key
    # 找到第2个1
    while index != 1:
        c_key &= (c_key - 1)  # 清除最后一位1
        index >>= 1
    new_key = (c_key & (-c_key)) ^ key  # 获取最后位置的1，1000 ^ 01(1)010
    return new_key


# 模式2匹配，两个key匹配
def match(key1, key2, keys, gates):
    # 1、匹配key有一个不同
    if bin(key1 ^ key2).count('1') == 1:
        last_index = key1 ^ key2
        big = key1 if bin(key1).count('1') > bin(key2).count('1') else key2
        small = key1 if big == key2 else key2
        for i in range(len(gates[big])):
            x1 = gates[big][i]
            # 2、value去除一位后，异或相差1
            # 求last_index是key中第几个1，对应x1中第几值要删除
            c_index = 1 << get_key(big, last_index)
            y1 = ((x1 >> 1) & (0b11111111 ^ (c_index - 1))) + ((c_index - 1) & x1)  # 保留last_index前后值，前面右移
            # print(y1, small)
            # 匹配，大的一点取反,小的删除
            for j in range(len(gates[small])):
                x2 = gates[small][j]
                if bin(y1 ^ x2).count("1") == 1:
                    # 1、大的变化，c_index为key不同的对应value位置
                    gates[big][i] = x1 ^ c_index
                    if x1 ^ c_index > (1 << bin(big).count('1')) - 1:
                        print('fault')
                    # 2、去除老的
                    gates[small].remove(x2)
                    if len(gates[small]) == 0:
                        del gates[small]
                        keys.remove(small)
                    # 3、加新的。
                    # 对应内部不同的，小的去掉不同的（已转化）
                    l_index = y1 ^ x2
                    # key:对应key的第last_index个1变成0
                    n_k = get_key2(small, l_index)
                    y2 = ((x2 >> 1) & ~(l_index - 1)) + ((l_index - 1) & x2)  # 保留last_index前后值，前面右移
                    # 产生新key不在gates中
                    # if n_k == 0:
                    #     return True
                    if n_k not in gates:
                        gates[n_k] = [y2]
                        keys.append(n_k)
                    # 产生相同的抵消了
                    elif y2 in gates[n_k]:
                        gates[n_k].remove(y2)
                        if len(gates[n_k]) == 0:
                            del gates[n_k]
                            keys.remove(n_k)
                    else:
                        gates[n_k].append(y2)
                    # keys.remove(small)
                    # oracle(gates)
                    # keys.clear()
                    # for key, _ in gates.items():
                    #     keys.append(key)
                    return True
    return False


if __name__ == '__main__':
    gates = {248: [0], 217: [1], 184: [4], 152: [0], 145: [1], 185: [20], 121: [25], 56: [0], 50: [1], 26: [3], 57: [1],
             11: [3], 59: [28], 187: [57], 234: [12], 203: [8], 171: [0], 107: [0], 123: [49], 251: [69], 150: [1],
             148: [0], 149: [11], 211: [8], 85: [0], 71: [2], 87: [20], 228: [3], 198: [2], 178: [9], 166: [11],
             182: [11], 113: [6], 99: [4], 51: [8], 117: [24], 243: [16], 241: [21], 53: [3], 245: [3], 167: [19],
             183: [49], 204: [12], 205: [2], 105: [4], 13: [0], 236: [24], 227: [1], 79: [19], 207: [12], 174: [0],
             143: [2], 15: [7], 239: [109], 141: [1], 29: [9], 220: [8], 120: [8], 116: [9], 92: [11], 252: [37],
             221: [42], 214: [4], 94: [12], 222: [32], 238: [14], 180: [5], 172: [5], 156: [5], 60: [5], 54: [9],
             30: [9], 63: [45], 125: [19], 95: [7], 111: [36], 127: [88], 219: [15], 31: [31], 223: [57]}
    gates = {37: [4], 45: [10]}
    gates = {118: [18], 86: [14]}
    print(gates)

    n_gates = mode2(gates)
    print(n_gates)
