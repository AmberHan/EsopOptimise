# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/1/12 20:55
# !@Author : DongHan Yang
# !@File   : mode1.py
# 按照模式1对gates进行修改，每次删除一个门
import copy
def mode1(gates):
    # n_gates = dict(sorted(gates.items(), key=lambda x: -bin(x[0]).count("1")))
    n_gates = copy.deepcopy(gates)
    # print(n_gates)
    # 初始化：取出所有key，方便两两比较
    keys = []
    for key, _ in n_gates.items():
        keys.append(key)
    while wh_key(keys, n_gates):
        pass
        # n_gates = dict(sorted(n_gates.items(), key=lambda x: -bin(x[0]).count("1")))
        # wh_key(keys, n_gates)
    return n_gates


# 每次匹配成功后，退出重新匹配
def wh_key(keys, n_gates):
    n = len(keys)
    for i in range(n):
        for j in range(i + 1, n):
            if match(keys[i], keys[j], keys, n_gates):
                return True
    return False


# 求last_index是key中第几个1，对应x1中第几值要删除
# 比如 101(1)010,1000, 返回1 代表是key中从小到大第2个1
def get_key(big, last_index):
    # 0111 & 101(1)010 = 10
    l_index = bin((last_index - 1) & big).count("1")
    return l_index


nums = []
nums1 = []


# 模式1匹配，两个key匹配
# key1,key2对比的键；keys所有的键；gates当前的门序列
def match(key1, key2, keys, gates):
    # 1、符合要求：key相差1个‘1’
    if bin(key1 ^ key2).count('1') == 1:  # 匹配
        last_index = key1 ^ key2  # 对应key差异位置
        big = key1 if bin(key1).count('1') > bin(key2).count('1') else key2
        small = key1 if big == key2 else key2
        # 两两比较里面的value，注意转换
        for i in range(len(gates[big])):
            x1 = gates[big][i]
            # 2、big的删除刚刚多余的，余下的相等
            # 转换去除多余的：求last_index是key中第几个1，c_index为转化后value的位置
            c_index = 1 << get_key(big, last_index)
            # x1去除c_index后的新值
            y1 = ((x1 >> 1) & (0b11111111 ^ (c_index - 1))) + ((c_index - 1) & x1)  # 保留last_index前后值，前面右移
            for j in range(len(gates[small])):
                # 匹配，大的多一点取反,小的删除
                if y1 == gates[small][j]:
                    gates[big][i] = x1 ^ c_index
                    if x1 ^ c_index > (1 << bin(big).count('1')) - 1:
                        print('fault')
                    gates[small].remove(y1)
                    if len(gates[small]) == 0:
                        # global nums,nums1
                        # nums.append(small)
                        # nums1.append(big)
                        del gates[small]
                        keys.remove(small)
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
    gates = {118: [18], 86: [10]}
    gates = {218: [9], 211: [15], 241: [29], 179: [27], 243: [0], 187: [4], 240: [10], 194: [4], 251: [5], 84: [2], 150: [5], 151: [3], 245: [50], 228: [9], 100: [5], 55: [31], 183: [20], 118: [10], 119: [44], 232: [12], 201: [13], 227: [24], 203: [28], 169: [14], 139: [14], 167: [23], 106: [8], 107: [30], 77: [14], 47: [6], 238: [44], 239: [109], 207: [31], 216: [10], 81: [5], 69: [5], 213: [23], 197: [15], 141: [15], 86: [12], 30: [12], 94: [30], 31: [15], 223: [94], 126: [44], 180: [14], 252: [42], 186: [14], 174: [30], 62: [22], 121: [25], 185: [25], 181: [27], 157: [13], 123: [57], 63: [26], 127: [71], 159: [55]}

    print(gates)
    n_gates = mode1(gates)
    print(n_gates)
    # print(nums)
    # print(nums1)
