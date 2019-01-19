import tqdm
import matplotlib.pyplot as plt

# 棋子的个数：士相车马炮卒，老将默认就有
chess = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 6, 6]


def load_data():
    f = open("data/棋型及状态总数.txt")
    a = [0] * 3 ** 10 * 36
    s = 0
    for i in range(len(a)):
        a[i] = int(f.readline())
        s += a[i]
    print("状态总数", s, float(s))
    return a


def parse(n):
    # 将数字转换为棋子表示
    a = [0] * 12
    for i in range(len(a) - 1, -1, -1):
        a[i] = n % chess[i]
        n //= chess[i]
    return a


def chess_cnt_state_cnt(a):
    # 棋子数和状态数之间的对应关系
    chess_cnt_map = [0] * 33
    for i in tqdm.tqdm(range(len(a))):
        chess_cnt = sum(parse(i)) + 2
        chess_cnt_map[chess_cnt] += a[i]
    for i, j in enumerate(chess_cnt_map):
        print(i, j)
    plt.plot(list(range(33)), chess_cnt_map)
    plt.show()


def most_state_chess(a):
    # 状态最多的局面是什么
    ma = a[0]
    mi = 0
    for i in range(1, len(a)):
        if a[i] > ma:
            ma = a[i]
            mi = i
    print("状态数最多的情况", parse(mi), ma)


def state_less(a):
    # 状态数较少的局面
    cnt = 0
    chess = [0] * 33
    with open('data/可枚举的棋型.txt', 'w')as f:
        for j, i in enumerate(a):
            if i < 1e8:
                cnt += 1
                chess_type = parse(j)
                chess_cnt = sum(chess_type) + 2
                chess[chess_cnt] += 1
                f.write('{} {}\n'.format(''.join(map(str, chess_type)), i))
    print("总共有局面", 3 ** 10 * 36)
    print('状态数较少的局面共有', cnt)
    for i, j in enumerate(chess):
        print(i, j)


a = load_data()
chess_cnt_state_cnt(a)
most_state_chess(a)
state_less(a)
"""
中国象棋棋子数和局面数对应关系
1 0
2 81
3 53352
4 17368920
5 3672575982
6 561878741934
7 65815888199136
8 6105519577653069
9 458441683302998262
10 28276281467420853535
11 1447613757679666620392
12 61990906560236481230212
13 2234284975648519824339780
14 68151060243661023020589312
15 1768583928750725279690825564
16 39248204713216436491550608772
17 748158492507863553499981189520
18 12286956306673455480869774269728
19 173972543879164666124034797298688
20 2119423639199325281433151350678528
21 22104946137817475450756733715349504
22 195715120391638442683661384178204672
23 1451859108730759676151580903528726528
24 8854504083425217829136792688577740800
25 43368283049804036804050691850523115520
26 166928807525329255164136546650688585728
27 494790429990658373961274364095719538688
28 1104346429752934661918096009259879759872
29 1797831119011557383961142180329119809536
30 2025498962529002731249530903863786209280
31 1424050840023000924108824993222484819968
32 479699516719060584838658530902374612992

中国象棋状态最多的棋子分布：
状态数最多的情况 [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 5]，也就是满员的情况下
状态数最多
状态数为：479699516719060584838658530902374612992
因为32枚棋子只有一种情况，就是满员情况

如果按照棋子个数来看：当棋子数是30枚时，能够摆出来的情况最多。因为
这30枚棋子可以有多种选择，不知道缺谁


"""
