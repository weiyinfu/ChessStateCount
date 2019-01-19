import math

"""
考虑升变，非常粗略的估计
假设象，卒可以到达棋盘上任意位置
"""
c_talbe = {}


def c(x, y):
    # 计算组合数
    k = (x, y)
    if not k in c_talbe:
        s = 1
        for i in range(1, y + 1):
            s = s * (x + 1 - i) / i
        c_talbe[k] = s
    return c_talbe[k]


def get_king():
    return 64 * 63 * get_queen_zu(62)


zu = {}


def get_queen_zu(free_space):
    if free_space not in zu:
        s = 0
        for w_zu in range(9):
            for b_zu in range(9):
                for w_queen in range(9 - w_zu + 1):  # 升变的卒子+一个本来就有的王后
                    for b_queen in range(9 - b_zu + 1):
                        ss = 1
                        t = free_space
                        ss *= c(t, w_zu)
                        t -= w_zu
                        ss *= c(t, b_zu)
                        t -= b_zu
                        ss *= c(t, w_queen)
                        t -= w_queen
                        ss *= c(t, b_queen)
                        t -= b_queen
                        ss *= get_jv_ma_xiang(t)
                        s += ss
        zu[free_space] = s
    return zu[free_space]


jv_ma_xiang = {}


def get_jv_ma_xiang(a):
    if a not in jv_ma_xiang:
        s = 0
        for r_jv in range(3):
            for b_jv in range(3):
                for r_ma in range(3):
                    for b_ma in range(3):
                        for r_xiang in range(3):
                            for b_xiang in range(3):
                                t = a
                                ss = 1
                                ss *= c(t, r_jv)
                                t -= r_jv
                                ss *= c(t, b_jv)
                                t -= b_jv
                                ss *= c(t, r_ma)
                                t -= r_ma
                                ss *= c(t, b_ma)
                                t -= b_ma
                                ss *= c(t, r_xiang)
                                t -= r_xiang
                                ss *= c(t, b_xiang)
                                t -= b_xiang
                                s += ss
        jv_ma_xiang[a] = s
    return jv_ma_xiang[a]


s = get_king()
print("状态数", s, "=10^{}".format(math.log10(s)))
bits_per_state = math.log2(s)
print("定长编码，每个状态的bit数", bits_per_state)
space = bits_per_state * s
print("定长编码存储全部状态所需空间", space / 8 / 1024 / 1024 / 1024 / 1024, "TB")
