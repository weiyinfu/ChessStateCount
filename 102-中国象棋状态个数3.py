"""
非常精确的中国象棋状态总数估计，老头照面属于合法状态
按照“将，士，相，卒，车马炮”的顺序进行布子，求中国象棋的总状态数

最终的结果已然超过了long类型，python自动转换为大整数类型
"""
import math
import scipy.special as sp

c_table = {}  # 组合数


def c(x, y):
    # 从x个数里面挑选y个
    k = (x, y)
    if not k in c_table:
        c_table[k] = sp.comb(x, y, exact=True)
    return c_table[k]


"""
0 1 2
3 4 5
6 7 8
将的九个位置
0，2，4，6，8表示将在士位上
1表示将在相位上
"""


def get_jiang():
    """
    将有三种位置：士位5个，相位1个，其它位置3个
    :return:
    """
    s = 0
    pos_count = [5, 1, 3]
    for r_jiang in range(3):  # r_jiang表示将的位置类型
        for b_jiang in range(3):
            s += get_shi(r_jiang, b_jiang) * pos_count[r_jiang] * pos_count[b_jiang]
    return s


shi = {}


def get_shi(r_jiang, b_jiang):
    k = (r_jiang, b_jiang)
    if not k in shi:
        s = 0
        r_shi_pos = 4 if r_jiang == 0 else 5
        b_shi_pos = 4 if b_jiang == 0 else 5
        for r_shi in range(3):
            for b_shi in range(3):
                s += c(r_shi_pos, r_shi) \
                     * c(b_shi_pos, b_shi) * \
                     get_xiang(r_jiang, b_jiang, r_space=45 - 1 - r_shi,
                               b_space=45 - 1 - b_shi)
        shi[k] = s
    return shi[k]


xiang = {}

"""
相的位置只跟未过河卒和老将有关系
相位
++0+++1++
+++++++++
2+++3+++4
+++++++++
++5+++6++
来一个第7位置，表示相死了
"""


def get_xiang(r_jiang, b_jiang, r_space, b_space):
    k = (r_jiang, b_jiang, r_space, b_space)
    if not k in xiang:
        s = 0
        r_xiang_pos = 6 if r_jiang == 1 else 7
        b_xiang_pos = 6 if b_jiang == 1 else 7
        for r_xiang in range(3):  # 相的总个数
            for b_xiang in range(3):
                for r_xiang_zu in range(r_xiang + 1):  # 相占用卒位的个数
                    for b_xiang_zu in range(b_xiang + 1):
                        s += c(2, r_xiang_zu) * c(2, b_xiang_zu) * \
                             c(r_xiang_pos - 2, r_xiang - r_xiang_zu) * \
                             c(b_xiang_pos - 2, b_xiang - b_xiang_zu) * \
                             get_zu(r_xiang_zu, b_xiang_zu, r_space - r_xiang, b_space - b_xiang)
        xiang[k] = s
    return xiang[k]


zu = {}


# 5列卒子位置，每列有两个卒位，被相占了used列，需要布下zu个卒子
def place_zu(used, zu):
    s = 0
    for i in range(min(used, zu) + 1):  # 有i个放在了used的列上，他们就不自由了，必然只有一种放法
        # 有zu-i个比较自由，每个卒自由度为2，从5-used列中选择zu-i列进行摆放
        s += 2 ** (zu - i) * c(5 - used, zu - i)
    return s


def get_zu(r_xiang_zu, b_xiang_zu, r_space, b_space):
    k = (r_xiang_zu, b_xiang_zu, r_space, b_space)
    if not k in zu:
        s = 0
        for r_zu in range(6):
            for b_zu in range(6):
                for r_zu_river in range(6 - r_zu):  # 因为是range，所以是6-r_zu
                    for b_zu_river in range(6 - b_zu):
                        s += place_zu(r_xiang_zu, r_zu) * \
                             place_zu(b_xiang_zu, b_zu) * \
                             c(r_space - r_zu, b_zu_river) * \
                             c(b_space - b_zu, r_zu_river) * \
                             get_jv_ma_pao(b_space + r_space - r_zu - r_zu_river - b_zu - b_zu_river)
        zu[k] = s
    return zu[k]


jv_ma_pao = {}


def get_jv_ma_pao(a):
    if not a in jv_ma_pao:
        s = 0
        for r_jv in range(3):
            for b_jv in range(3):
                for r_ma in range(3):
                    for b_ma in range(3):
                        for r_pao in range(3):
                            for b_pao in range(3):
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
                                ss *= c(t, r_pao)
                                t -= r_pao
                                ss *= c(t, b_pao)
                                t -= b_pao
                                s += ss
        jv_ma_pao[a] = s
    return jv_ma_pao[a]


s = get_jiang()
print("状态数", s, "=", float(s))
bits_per_state = math.log2(s)
print("定长编码，每个状态的bit数", bits_per_state)
space = bits_per_state * s
print("定长编码存储全部状态所需空间", space / 8 / 1024 / 1024 / 1024 / 1024, "TB")

"""
状态数 7.547040878332445e+39 =10^39.877776702341485
定长编码，每个状态的bit数 132.4711067891529
定长编码存储全部状态所需空间 1.1366010518664549e+29 TB
"""
