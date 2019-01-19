import math

"""
简单粗略地估计中国象棋状态总数
"""


def c(x, y):
    # 定义组合数
    ans = 1
    for i in range(1, y + 1):
        ans = ans * (x + 1 - i) / i
    return ans


def get_zu():
    """
    卒子分为两类，过河卒和未过河卒
    """
    s = 0
    for i in range(0, 6):  # 过河的有几个
        for j in range(0, 6 - i):  # 没过河的有几个
            s += c(45, i) * c(5, j) * 2 ** j
    return s


"""
9宫格内，将士可以有：
c(9,3)*3:从九个位置挑选3个，其中一个放“将”，另外两个放“士”
c(9,2)*2:从九个位置挑选2个，其中一个放“将”，另外一个放“士”
"""
jiang_shi = c(9, 3) * 3 + c(9, 2) * 2 + c(9, 1) * 1
"""
相有七个位置，枚举相的个数：0,1,2
"""
xiang = c(7, 0) + c(7, 1) + c(7, 2)
zu = get_zu()
"""
枚举“车马炮”的个数
"""
jv = c(90, 0) + c(90, 1) + c(90, 2)
ma = jv
pao = jv
s1 = jiang_shi * xiang * zu * jv * ma * pao
s = s1 ** 2  # 象棋是两个人的游戏，上面只考虑了一个人

print("状态数", s, "=10^", math.log10(s))
bits_per_state = math.log2(s)
print("定长编码，每个状态的bit数", bits_per_state)
space = bits_per_state * s
print("定长编码存储全部状态所需空间", space / 8 / 1024 / 1024 / 1024 / 1024, "TB")
