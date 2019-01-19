import math
import sys
import time

import scipy.special as sp

"""
给定各个棋种的棋子数，求局面数
"""
c_map = dict()


def c(n, k):
    t = (n, k)
    if t not in c_map:
        c_map[t] = sp.comb(n, k, exact=True)
    return c_map[t]


jv_ma_pao_map = dict()


def get_jv_ma_pao(free, jv_ma_pao):
    """
    给定剩余空间，计算车马炮的个数
    :param free: 棋盘上剩余空间数
    :param jv_ma_pao: 车马炮按照顺序排列的元组
    :return:
    """
    k = (free, jv_ma_pao)
    if (free, jv_ma_pao) not in jv_ma_pao_map:
        s = 1
        for i in jv_ma_pao:
            s *= c(free, i)
            free -= i
        jv_ma_pao_map[k] = s
    return jv_ma_pao_map[k]


zu_map = dict()


def place_zu(used, zu):
    # 5列卒子位置，每列有两个卒位，被相占了used列，需要布下zu个卒子
    if (used, zu) not in zu_map:
        s = 0
        for i in range(min(used, zu) + 1):  # 有i个放在了used的列上，他们就不自由了，必然只有一种放法
            # 有zu-i个比较自由，每个卒自由度为2，从5-used列中选择zu-i列进行摆放
            s += 2 ** (zu - i) * c(5 - used, zu - i)
        zu_map[(used, zu)] = s
    return zu_map[(used, zu)]


zu_map2 = dict()


def get_zu(r_xiang_zu, b_xiang_zu,
           red_free, black_free,
           r_zu, b_zu,
           jv_ma_pao):
    k = (r_xiang_zu, b_xiang_zu, red_free, black_free, r_zu, b_zu, jv_ma_pao)
    if k not in zu_map2:
        s = 0
        for r_zu_river in range(r_zu + 1):
            for b_zu_river in range(b_zu + 1):
                s += place_zu(r_xiang_zu, r_zu - r_zu_river) * \
                     place_zu(b_xiang_zu, b_zu - b_zu_river) * \
                     c(red_free - (r_zu - r_zu_river), b_zu_river) * \
                     c(black_free - (b_zu - b_zu_river), r_zu_river) * \
                     get_jv_ma_pao(red_free + black_free - r_zu - b_zu, jv_ma_pao)
        zu_map2[k] = s
    return zu_map2[k]


xiang_map = dict()


def get_xiang(r_jiang, b_jiang,
              red_free, black_free,
              r_xiang, b_xiang,
              r_zu, b_zu,
              jv_ma_pao):
    k = (r_jiang, b_jiang, red_free, black_free, r_xiang, b_xiang, r_zu, b_zu, jv_ma_pao)
    if k not in xiang_map:
        r_xiang_pos = 6 if r_jiang == 1 else 7
        b_xiang_pos = 6 if b_jiang == 1 else 7
        s = 0
        for r_xiang_zu in range(r_xiang + 1):  # 红相占用卒位的个数
            for b_xiang_zu in range(b_xiang + 1):  # 黑相占用卒位的个数
                s += c(2, r_xiang_zu) * \
                     c(r_xiang_pos - 2, r_xiang - r_xiang_zu) * \
                     c(2, b_xiang_zu) * \
                     c(b_xiang_pos - 2, b_xiang - b_xiang_zu) * \
                     get_zu(
                         r_xiang_zu, b_xiang_zu,
                         red_free - r_xiang, black_free - b_xiang,
                         r_zu, b_zu,
                         jv_ma_pao)
        xiang_map[k] = s
    return xiang_map[k]


shi_map = dict()


def get_shi(r_jiang, b_jiang,
            r_shi, b_shi,
            r_xiang, b_xiang,
            r_zu, b_zu,
            jv_ma_pao):
    k = (r_jiang, b_jiang, r_shi, b_shi, r_xiang, b_xiang, r_zu, b_zu, jv_ma_pao)
    if k not in shi_map:
        r_shi_pos = 4 if r_jiang == 0 else 5
        b_shi_pos = 4 if b_jiang == 0 else 5
        shi_map[k] = c(r_shi_pos, r_shi) \
                     * c(b_shi_pos, b_shi) \
                     * get_xiang(r_jiang, b_jiang,
                                 45 - 1 - r_shi, 45 - 1 - b_shi,
                                 r_xiang, b_xiang,
                                 r_zu, b_zu,
                                 jv_ma_pao)
    return shi_map[k]


jiang_map = dict()


def place(r_shi, b_shi,
          r_xiang, b_xiang,
          r_zu, b_zu,
          r_jv, b_jv,
          r_ma, b_ma,
          r_pao, b_pao):
    """
    将有三种位置：士位，相位，九宫中的其它位置，三种位置分别有5,1,3个
    """
    jv_ma_pao = tuple(sorted([r_jv, b_jv, r_ma, b_ma, r_pao, b_pao]))
    k = (r_shi, b_shi, r_xiang, b_xiang, r_zu, b_zu, jv_ma_pao)
    if k not in jiang_map:
        s = 0
        pos_count = [5, 1, 3]
        for r_jiang in range(3):  # 枚举红将的三种位置
            for b_jiang in range(3):  # 枚举黑将的三种位置
                s += get_shi(r_jiang, b_jiang,
                             r_shi, b_shi,
                             r_xiang, b_xiang,
                             r_zu, b_zu,
                             jv_ma_pao) * pos_count[r_jiang] * pos_count[b_jiang]
        jiang_map[k] = int(s)
    return jiang_map[k]
 
total_count = 3 ** 10 * 36
s = 0
iter_count = 0
beg = time.time()
a = [0] * total_count
for r_shi in range(3):  # 红士的个数
    for b_shi in range(3):  # 黑士的个数
        for r_xiang in range(3):  # 红相的个数
            for b_xiang in range(3):  # 黑相的个数
                for r_jv in range(3):  # 红车的个数
                    for b_jv in range(3):  # 黑车的个数
                        for r_ma in range(3):  # 红马的个数
                            for b_ma in range(3):  # 黑马的个数
                                for r_pao in range(3):  # 红炮的个数
                                    for b_pao in range(3):  # 黑炮的个数
                                        for r_zu in range(6):  # 红卒的个数
                                            for b_zu in range(6):  # 黑卒的个数
                                                cnt = place(r_shi, b_shi,
                                                            r_xiang, b_xiang,
                                                            r_zu, b_zu,
                                                            r_jv, b_jv,
                                                            r_ma, b_ma,
                                                            r_pao, b_pao)
                                                a[iter_count] = cnt
                                                s += cnt
                                                iter_count += 1
                                                ratio = iter_count / total_count
                                                sys.stdout.write('\r已完成{},还需时间{}秒'.format(ratio,
                                                                                          (
                                                                                              time.time() - beg) / ratio * (
                                                                                              1 - ratio)))
end = time.time()
print("\n总共用时", end - beg, "秒")
"""
打表结果的顺序为：for循环的顺序:士相车马炮卒
"""
with open("data/棋子个数及状态总数.txt", "w") as f:
    for i in a:
        f.write(str(i))
        f.write('\n')
print("状态数", int(s), "=10^{}".format(math.log10(s)))
bits_per_state = math.log2(s)
print("定长编码，每个状态的bit数", bits_per_state)
space = bits_per_state * s
print("定长编码存储全部状态所需空间", space / 8 / 1024 / 1024 / 1024 / 1024, "TB")
"""
一种假设：
如果局面A轮到我走并且我方已经是必胜
棋子越多越好，我方添加棋子之后依然是必胜状态

实际上这个假设是错误的：
* 棋子多有可能会蹩脚
* 老将行动更加不灵活
* 我方战斗人员行动更加不便，给敌人以还手之机

但是百分之九十九的情况下这个假设是正确的，
依据这个假设，可以直接忽略掉大量的后续状态
"""
