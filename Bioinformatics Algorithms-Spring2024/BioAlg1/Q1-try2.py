from collections import deque
from copy import deepcopy

maxn = 7005
maxm = 10500
infinity = 10**9

class Edge:
    def __init__(self, v=0, ne=0, cap=0, flow=0, costt=0, u=0):
        self.v = v
        self.ne = ne
        self.cap = cap
        self.flow = flow
        self.cost = costt
        self.u = u

ed = [Edge()] * maxm
head = [0] * maxn
cnt = 0
pre = [0] * maxn
dis = [0] * maxn
vis = [0] * maxn

# def initiate(x):
#     global cnt, head
#     cnt = 0
#     for i in range(x + 1):
#         head[i] = -1

def add(u, v, cap, ccost):
    global ed, cnt, head
    ed[cnt].v = v
    ed[cnt].cap = cap
    ed[cnt].flow = 0
    ed[cnt].u = u
    ed[cnt].cost = ccost
    ed[cnt].ne = head[u]
    head[u] = cnt
    cnt += 1

    ed[cnt].v = u
    ed[cnt].cap = 0
    ed[cnt].flow = 0
    ed[cnt].u = v
    ed[cnt].cost = -1 * ccost
    ed[cnt].ne = head[v]
    head[v] = cnt
    cnt += 1

def spfa(st, en): # returns bool
    global dis, vis, pre, head, ed
    q = deque()
    for s in range(en + 1):
        dis[s] = infinity
        vis[s] = 0
        pre[s] = -1
    dis[st] = 0
    vis[st] = 1
    q.append(st)
    print("st in spfa:", st)
    while len(q) > 0:
        uu_ = q.popleft()
        vis[uu_] = 0
        s = head[uu_]
        print("head[st]:", head[st])
        print("s:", s)
        while s != -1:
            print("here!")
            vv = ed[s].v
            if ed[s].cap > ed[s].flow and dis[vv] > dis[uu_] + ed[s].cost:
                dis[vv] = dis[uu_] + ed[s].cost
                pre[vv] = s
                if vis[vv] == 0:
                    vis[vv] = 1
                    q.append(vv)
            s = ed[s].ne
    print("pre[en]:", pre[en])
    if pre[en] == -1:
        return 0
    return 1

def mcmf(st, en):
    global cost, pre, ed
    flow = 0
    while spfa(st, en) != 0:
        minn = infinity
        s = pre[en]
        print(s)
        while s != 1:
            print("here2")
            if minn > ed[s].cap - ed[s].flow:
                minn = ed[s].cap - ed[s].flow
            s = pre[ed[s^1].v]
        s = pre[en]
        while s != -1:
            ed[s].flow += minn
            ed[s^1].flow -= minn
            cost += ed[s].cost*minn
            s = pre[ed[s^1].v]
        flow += minn
    return flow

thead = [0] * maxn
tcnt = 0

while True:
    insplit = [ch for ch in input().split(" ") if len(ch) > 0]
    if len(insplit) == 0:
        break
    n, m, k = tuple(map(int, insplit))
    if n == 0 and m == 0 and k == 0:
        break

    st = 0
    en = k * (n + m) + 1
    cnt = 0
    for i in range(en + 1):
        head[i] = -1
    sum = 0
    for i in range(n):
        temp = list(map(int, input().split(" ")))
        for j in range(1, k + 1):
            a = temp[j - 1]
            add(k * m + k * i + j, en, a, 0)
            sum += a

    for i in range(m):
        temp = list(map(int, input().split(" ")))
        for j in range(1, k + 1):
            a = temp[j - 1]
            add(st, k * i + j, a, 0)
    tcnt = cnt
    for i in range(en + 1):
        thead[i] = deepcopy(head[i])
    cost = 0
    need = 0
    for u_ in range(1, k + 1):
        cnt = tcnt
        for i in range(en + 1):
            head[i] = deepcopy(thead[i])
        for i in range(n):
            temp = list(map(int, input().split(" ")))
            for j in range(m):
                a = k * m + k * i + u_
                b = k * j + u_
                c = temp[j]
                add(b, a, infinity, c)
        print("st:", st)
        need += mcmf(st, en)
    if need != sum:
        print("cost:", cost)
        print(-1)
    else:
        print(cost)
    dummy = input()