# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/2/22 14:26
# !@Author : DongHan Yang
# !@File   : CPMN.py

# 统计出，key1和key2的CPMN位置
def getCpmn(key1, g1, key2, g2):
    CP = key1 & key2
    MN = key1 ^ key2
    M = key1 & MN
    N = key2 & MN
    # g1 g2得到具有相同控制线的正负
    g1_CP_value = removeKeyValue(CP, key1, g1)
    g2_CP_Value = removeKeyValue(CP, key2, g2)
    C_value = ((1 << bin(CP).count('1')) - 1) ^ (g1_CP_value ^ g2_CP_Value)
    C = getValueKey(CP, C_value)
    P = CP ^ C
    return C, P, M, N


# 返回p的数目
def pKey(key1, g1, key2, g2):
    CP = key1 & key2
    # g1 g2得到具有相同控制线的正负
    g1_CP_value = removeKeyValue(CP, key1, g1)
    g2_CP_Value = removeKeyValue(CP, key2, g2)
    C_value = ((1 << bin(CP).count('1')) - 1) ^ (g1_CP_value ^ g2_CP_Value)
    C = getValueKey(CP, C_value)
    P = CP ^ C
    return P


# 返回CP,M,N数目
def getCpmnNumber(key1, key2):
    CP = key1 & key2
    MN = key1 ^ key2
    M = key1 & MN
    N = key2 & MN
    return CP, M, N


# 计算出相同控制线CP在key中的value，移除非CP的1；计算CP下的value
# re：   110010
# Key:   111011
# value: 010 10
# output:01  1
def removeKeyValue(removeKey, key, value):
    sums = 0
    counts = 0
    while key:
        last_key_one = key & (-key)  # 获取最后一个1
        if removeKey & last_key_one != 0:  # 为CP，考虑
            if value % 2:
                sums += (1 << counts)
            counts += 1
        value >>= 1  # 去除最低位
        key &= (key - 1)  # 清除最后一个1
    return sums


# 在value中插入
# in：   111011
# Key:   111001
# value: 010  0
# output:010 10
def insertKeyValue(insertKey, key, value):
    sums = 0
    counts = 0
    while insertKey:
        last_key_one = insertKey & (-insertKey)  # 获取最后一个1
        if key & last_key_one != 0:  # 原有的
            if value % 2:
                sums += (1 << counts)
            value >>= 1  # 去除最低位
        else:
            sums += (1 << counts)
        counts += 1
        insertKey &= (insertKey - 1)  # 清除最后一个1
    # print(sums)
    return sums


# insertKeyValue(0b111111, 0b111001, 0b0100)


# 将value中的cKey取反
# cKey： 110010
# Key:   111011
# value: 010 10
# output:100 00
def changeValue(cKey, key, value):
    copy_key = key
    count_key = 0
    while copy_key:
        last_key_one = copy_key & (-copy_key)  # 获取最后一个1
        if cKey & last_key_one != 0:  # 为1，对应的value的值取反
            value ^= (1 << count_key)
        count_key += 1
        copy_key &= (copy_key - 1)  # 清除最后一个1
    return value


# value中的1表示为共同节点，目标获取value==1对应的key,即C的key
# 计算出value中为0，对应的key的值置为0;计算C对应线
# value:   01 01  0101
# key:     110110 11110000
# output:  010010 01010000(由key->output)
def getValueKey(key, value):
    copy_key = key
    while copy_key:
        last_key_one = copy_key & (-copy_key)  # 获取最后一个1
        if value % 2 == 0:  # 为0，对应的key的值置为0
            key ^= last_key_one
        value >>= 1  # 去除最低位
        copy_key &= (copy_key - 1)  # 清除最后一个1
    print(bin(key))
    return key

# getValueKey(0b11011011110000, 0b01010101)
# a = getCpmn(0b111111000, 0b110010, 0b111100111, 0b0110011)
# print(a)
