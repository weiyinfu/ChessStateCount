import scipy.special as sp
import timeit
import random

"""
scipy中的计算组合数默认exact=false，时间复杂度较高，
这是由于scipy默认使用的是浮点数计算的，
使用exact参数可以保证为int运算，时间效率大约能提高5倍，
比手写的还快，因为scipy调用了c语言实现
"""
a = []
for i in range(1000000):
    n = random.randint(3, 100)
    k = random.randint(0, n)
    a.append((n, k))


def his():
    print("his")
    for n, k in a:
        sp.comb(n, k, exact=True)


def c(n, k):
    s = 1
    k = min(k, n - k)
    for i in range(1, k):
        s = s * (n + 1 - i) // i
    return s


def mine():
    print("mine")
    for n, k in a:
        c(n, k)


he = timeit.timeit(his, number=1)
me = timeit.timeit(mine, number=1)
print(he)
print(me)
