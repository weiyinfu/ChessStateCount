import math

"""
更加精确一些的估计
"""


def c(x, y):
    ans = 1
    for i in range(1, y + 1):
        ans = ans * (x + 1 - i) / i
    return ans


def get_zu():
    s = 0
    for i in range(0, 6):  # 过河的有几个
        for j in range(0, 6 - i):  # 没过河的有几个
            s += c(45, i) * c(5, j) * 2 ** j
    return s


def get_jv_ma_pao():
    s = 0
    a = 89
    for r_jv in range(3):
        for b_jv in range(3):
            for r_pao in range(3):
                for b_pao in range(3):
                    for r_ma in range(3):
                        for b_ma in range(3):
                            t = a
                            ss = 1
                            ss *= c(t, r_jv)
                            t -= r_jv
                            ss *= c(t, b_jv)
                            t -= b_jv
                            ss *= c(t, r_pao)
                            t -= r_pao
                            ss *= c(t, b_pao)
                            t -= b_pao
                            ss *= c(t, r_ma)
                            t -= r_ma
                            ss *= c(t, b_ma)
                            t -= b_ma
                            s += ss
    return s


jiang_shi = c(9, 3) + c(9, 2) + c(9, 1)
xiang = c(7, 0) + c(7, 1) + c(7, 2)
zu = get_zu()
s = (jiang_shi * xiang * zu) ** 2 * get_jv_ma_pao()

print("状态数", s, "=10^", math.log10(s))
bits_per_state = math.log2(s)
print("定长编码，每个状态的bit数", bits_per_state)
space = bits_per_state * s
print("定长编码存储全部状态所需空间", space / 8 / 1024 / 1024 / 1024 / 1024, "TB")
