import numpy as np
from collections import deque

def fill_arr(arr, val, dtype=int):
    arrnp = np.array(arr)
    arrnp = np.full(arrnp.shape, val, dtype=dtype)
    return arrnp.tolist()

# print(fill_arr([[1, 2], [4, 5], [7, 8]], 6., float))

maxn = 200
maxl = 200000
infinity = 2**30

class Line:
    def __init__(self, v=0, nxt=0, w=0, fb=0, fy=0):
        self.v = v
        self.nxt = nxt
        self.w = w
        self.fb = fb
        self.fy = fy

e = [Line()] * maxl
h = [0] * maxn
cnt = 1
cost = 0
ff = 0

tot = [0] * maxn
need = np.full((maxn, maxn), 0, dtype=int).tolist()
have = np.full((maxn, maxn), 0, dtype=int).tolist()
Cost = np.full((maxn, maxn, maxn), 0, dtype=int).tolist()

pe = [0] * maxn
pr = [0] * maxn
Ans = 0

def Add(u, v, w, fy):
    global e, cnt, h
    e[cnt] = Line(v, h[u], w, cnt + 1, fy)
    h[u] = cnt
    cnt += 1
    e[cnt] = Line(u, h[v], 0, cnt - 1, -1 * fy)
    h[v] = cnt
    cnt += 1

dis = [0] * maxn
S = 0
T = 0
N = 0
M = 0
K = 0

vis = [False] * maxn

def SPFA(): # returns boolean
    global dis, S, vis, h, e, pe, pr, T, infinity, ff, cost
    dis = fill_arr(dis, 63)
    dis[S] = 0
    Q = deque()
    while len(Q) > 0:
        Q.popleft()
    Q.append(S)
    vis = fill_arr(vis, 0)
    while len(Q) > 0:
        u = Q[0]
        Q.popleft()
        vis[u] = False
        i = h[u]
        while i != 0:
            f = dis[u] + e[i].fy
            v = e[i].v
            if e[i].w != 0 and dis[v] > f:
                dis[v] = f
                pe[v] = i
                pr[v] = u
                if not vis[v]:
                    vis[v] = True
                    Q.append(v)
            i = e[i].nxt
    if dis[T] == dis[T + 1]:
        return False
    ree = infinity
    v = T
    while v != S:
        ree = min(ree, e[pe[v]].w)

        v = pr[v]
    v = T
    while v != S:
        e[pe[v]].w -= ree
        e[e[pe[v]].fb].w += ree

        v = pr[v]
    ff += ree
    cost += ree*dis[T]
    return True

while True:
    while True:
        insplit = [ch for ch in input().split(" ") if len(ch) > 0]
        if len(insplit) == 3:
            break
    N, M, K = tuple(map(int, insplit))
    if N == 0 and M == 0 and K == 0:
        break
    tot = fill_arr(tot, 0)
    for i in range(1, N + 1):
        temp = list(map(int, input().split(" ")))
        for j in range(1, K + 1):
            need[i][j] = temp[j - 1]
            tot[j] += need[i][j]

    for i in range(1, M + 1):
        temp = list(map(int, input().split(" ")))
        for j in range(1, K + 1):
            have[i][j] = temp[j - 1]
            tot[j] -= have[i][j]

    for i in range(1, K + 1):
        for j in range(1, N + 1):
            temp = list(map(int, input().split(" ")))
            for k in range(1, M + 1):
                Cost[i][j][k] = temp[k - 1]

    # print("need:", need)
    # print("have:", have)
    # print("Cost:", Cost)

    S = 0
    T = N + M + 1
    fl = True
    for k in range(1, K + 1):
        if tot[k] > 0:
            fl = False
            break
    if not fl:
        fl = True
        print(-1)
        continue

    Ans = 0
    for k in range(1, K + 1):
        cnt = 1
        h = fill_arr(h, 0)
        for j in range(1, M + 1):
            Add(S, j, have[j][k], 0)
            for i in range(1, N + 1):
                Add(j, i + M, have[j][k], Cost[k][i][j])
        for i in range(1, N + 1):
            Add(i + M, T, need[i][k], 0)
        ff = 0
        cost = ff
        while SPFA():
            do_nothing = True
        Ans += cost
    print(Ans)

    # dummy = input()