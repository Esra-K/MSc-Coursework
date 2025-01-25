import numpy as np
from collections import deque

from Bio.Align.Applications import ClustalwCommandline
# def fill_arr(arr, val, dtype=int):
#     arrnp = np.array(arr)
#     arrnp = np.full(arrnp.shape, val, dtype=dtype)
#     return arrnp.tolist()
# print(fill_arr([[1, 2], [4, 5], [7, 8]], 6., float))

maxn = 10000
s, t = 0, 0
head = [0] * maxn
dis = [0] * maxn
pre = [0] * maxn
last = [0] * maxn
flow = [0] * maxn
vis = [0] * maxn

maxflow = 0
mincost = 0
tot = -1

class Edge:
    def __init__(self, u=0, v=0, w=0, c=0, nxt=0):
        self.u = u
        self.v = v
        self.w = w
        self.c = c
        self.nxt = nxt
es = [Edge()] * maxn

def add(u, v, w, c):
    global tot, head
    tot += 1
    es[tot] = Edge(u, v, w, c, head[u])
    head[u] = tot

def addedge(u, v, w, c):
    add(u, v, w, c)
    add(v, u, 0, -1 * c)

def spfa():
    global dis, flow, vis, s, t
    dis = [10**6] * maxn # fill_arr(dis, 10**9)
    flow = [10**3] * maxn # fill_arr(flow, 10**3)
    vis = [0] * maxn # fill_arr(vis, 0)
    q = deque()
    q.append(s)
    vis[s] = 1
    dis[s] = 0
    pre[t] = -1
    while len(q) > 0:
        # print("spfa")
        u = q.popleft()
        vis[u] = 0
        i = head[u]
        while i != -1:
            v = es[i].v
            w = es[i].w
            c = es[i].c
            if w > 0 and dis[v] > dis[u] + c:
                dis[v] = dis[u] + c
                flow[v] = min(flow[u], w)
                pre[v] = u
                last[v] = i
                if v == t:
                    return 1
                if not vis[v]:
                    q.append(v)
                    vis[v] = 1
            i = es[i].nxt
    return 0

def mincostmaxflow():
    global t, maxflow, mincost, flow, dis, s, es, last, flow
    while spfa():
        # print("mcmf")
        now = t
        maxflow += flow[t]
        mincost += flow[t] * dis[t]
        while now != s:
            es[last[now]].w -= flow[t]
            es[last[now] ^ 1].w += flow[t]
            now = pre[now]

while True:
    insplit = [ch for ch in input().split(" ") if len(ch) > 0]
    n, m, k = tuple(map(int, insplit))
    if n == 0 and m == 0 and k == 0:
        break
    demand = [[0 for j in range(k)] for i in range(n)]
    for i in range(n):
        demand[i] = list(map(int, input().split(" ")))
    # print(f"demand: {demand}")
    supply = [[0 for j in range(k)] for i in range(m)]
    for i in range(m):
        supply[i] = list(map(int, input().split(" ")))
    # print(f"supply: {supply}")
    cost = [[[0 for l in range(m)] for j in range(n)] for i in range(k)]
    for i in range(k):
        for j in range(n):
            cost[i][j] = list(map(int, input().split(" ")))
    # print(f"cost: {cost}")
    # print(demand)
    # print(supply)
    # print(cost)
    s = n + m + 5
    t = s + 1
    ans = 0
    flag = 1
    for i in range(k):
        head = [-1] * maxn # fill_arr(head, -1)
        tot = -1
        maxflow = 0
        mincost = 0
        M = 0
        for j in range(n):
            addedge(j + m, t, demand[j][i], 0)
            M += demand[j][i]
        for j in range(m):
            addedge(s, j, supply[j][i], 0)
        for j in range(n):
            for l in range(m):
                addedge(l, j + m, supply[l][i], cost[i][j][l])
        mincostmaxflow()
        if maxflow < M:
            flag = 0
            break
        else:
            ans += mincost
        # print(f"k: {k}")
    if flag:
        # print(f"flag true")
        print(ans)
    else:
        # print("flag false")
        print(-1)
    # dummy = input()