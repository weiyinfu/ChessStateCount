"""
理论上讲，国际象棋状态数比中国象棋状态数多
不考虑小兵升变王后，就已经比中象多
在国际象棋中，行动范围最受限制的是卒子和象，其余棋子可以到达棋盘上的任意位置
所以先考虑卒子和象，再考虑其它棋子
其次需要考虑象，国际象棋中的象只能到达棋盘上一半的空间（奇数号空间或者偶数号空间）
国际象棋中两个象是不等价的

将棋盘分为六种区域：
第一行是敌方卒子无法到达的地方
最后一行是我方卒子无法到达的地方
奇数空间是偶数象无法到达的地方
偶数空间是偶数象无法到达的地方

"""
import math

import scipy.special as sp


def c(n, k):
    return sp.comb(n, k, exact=True)


def get_zu():
    s = 0
    for w_zu in range(9):
        for b_zu in range(9):
            for w_zu_middle in range(w_zu + 1):
                for b_zu_middle in range(b_zu + 1):
                    for w_zu_middle_odd in range(w_zu_middle + 1):
                        for b_zu_middle_odd in range(b_zu_middle + 1):
                            for w_zu_final_odd in range(w_zu - w_zu_middle + 1):
                                for b_zu_final_odd in range(b_zu - b_zu_middle + 1):
                                    # 中间区域白卒子偶数位置个数
                                    w_zu_middle_even = w_zu_middle - w_zu_middle_odd
                                    # 中间区域黑卒子偶数位置个数
                                    b_zu_middle_even = b_zu_middle - b_zu_middle_odd
                                    # 底线区偶数位置白卒个数
                                    w_zu_final_even = w_zu - w_zu_middle - w_zu_final_odd
                                    # 底线区偶数位置黑卒个数
                                    b_zu_final_even = b_zu - b_zu_middle - b_zu_middle_odd
                                    s += c(24, w_zu_middle_odd) \
                                         * c(24 - w_zu_middle_odd, b_zu_middle_odd) \
                                         * c(24, w_zu_middle_even) \
                                         * c(24 - w_zu_middle_even, b_zu_middle_even) \
                                         * c(4, w_zu_final_odd) \
                                         * c(4, b_zu_final_odd) \
                                         * c(4, w_zu_final_even) \
                                         * c(4, w_zu_final_even) \
                                         * get_xiang(
                                        32 - w_zu_final_odd - b_zu_final_odd - w_zu_middle_odd - b_zu_middle_odd,
                                        32 - w_zu_final_even - b_zu_final_even - w_zu_middle_even - b_zu_middle_even)
    return s


xiang = dict()


def get_xiang(odd_space, even_space):
    k = (odd_space, even_space)
    if k not in xiang:
        s = 0
        for w_xiang_odd in range(2):
            for w_xiang_even in range(2):
                for b_xiang_odd in range(2):
                    for b_xiang_even in range(2):
                        s += c(odd_space, w_xiang_odd) \
                             * c(odd_space - w_xiang_odd, b_xiang_odd) \
                             * c(even_space, w_xiang_even) \
                             * c(even_space - w_xiang_even, b_xiang_even) \
                             * get_king_queen_jv_ma(
                            odd_space + even_space - w_xiang_even - b_xiang_even - b_xiang_odd - w_xiang_odd)
        xiang[k] = s
    return xiang[k]


king_queen_jv_ma = dict()


def get_king_queen_jv_ma(free):
    if free not in king_queen_jv_ma:
        s = 0
        for w_queen in range(2):
            for b_queen in range(2):
                for w_jv in range(3):
                    for b_jv in range(3):
                        for w_ma in range(3):
                            for b_ma in range(3):
                                # 两个king是必须要有的
                                s += c(free, 2) * 2 \
                                     * c(free - 2, w_queen) \
                                     * c(free - 2 - w_queen, b_queen) \
                                     * c(free - 2 - w_queen - b_queen, w_jv) \
                                     * c(free - 2 - w_queen - b_queen - w_jv, b_jv) \
                                     * c(free - 2 - w_queen - b_queen - w_jv - b_jv, w_ma) \
                                     * c(free - 2 - w_queen - b_queen - w_jv - b_jv - w_ma, b_ma)
        king_queen_jv_ma[free] = s
    return king_queen_jv_ma[free]


s = get_zu()
print("状态数", s, "=10^{}".format(math.log10(s)))
bits_per_state = math.log2(s)
print("定长编码，每个状态的bit数", bits_per_state)
space = bits_per_state * s
print("定长编码存储全部状态所需空间", space / 8 / 1024 / 1024 / 1024 / 1024, "TB")
