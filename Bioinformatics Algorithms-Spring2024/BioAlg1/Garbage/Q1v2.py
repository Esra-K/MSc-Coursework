from collections import deque

def clean(arr, val):
    for index in range(len(arr)):
        arr[index] = val
    return arr

class Dots:
    def __init__(self, x, y):
        self.x = x # int
        self.y = y # int

dots = [Dots(0, 0)] * 110
dott = [Dots(0, 0)] * 110

class Node:
    def __init__(self, v=0, w=0, cost=0, nxt=0):
        self.v = v # int
        self.w = w # int
        self.cost = cost # int
        self.nxt = nxt # int

bigint = 100010
edge = [Node(0, 0, 0, 0)] * (bigint * 2)

head = [0] * bigint
ecnt = 0
dis = [0] * bigint
flow = [0] * bigint
pre = [0] * bigint
last = [0] * bigint

vis = [0] * bigint
maxw = 0
mincost = 0
# n = 0
# m = 0
# k = 0
s = 0
t = 0

def intt():
    global head, last, pre, ecnt, maxw, mincost
    head = clean(head, -1)
    last = clean(last, 0)
    pre = clean(pre, -1)
    ecnt = 0
    maxw = 0
    mincost = 0

def add(u, v, w, cost):
    global edge, ecnt, head
    edge[ecnt] = Node(v, w, cost, head[u])
    head[u] = ecnt
    ecnt += 1
    edge[ecnt] = Node(u, 0, -1 * cost, head[v])

infinity = 1061109567
def spfa():
    global infinity, dis, flow, vis, s, t
    dis = clean(dis, infinity)
    flow = clean(flow, infinity)
    vis = clean(vis, 0)
    q = deque()
    q.append(s)
    vis[s] = 1
    dis[s] = 0
    pre[t] = -1
    while len(q) > 0:
        uu = q[0]
        q.popleft()
        vis[uu] = 0
        # for loop
        i = head[uu]
        while i + 1 > 0:
            temp = edge[i].v
            if dis[temp] > dis[uu] + edge[i].cost and edge[i].w > 0:
                dis[temp] = dis[uu] + edge[i].cost
                pre[temp] = uu
                last[temp] = i
                flow[temp] = min(edge[i].w, flow[uu])
                if vis[temp] == 0:
                    vis[temp] = 1
                    q.append(temp)
            # end of loop
            i = edge[i].nxt
    return pre[t] != -1

def MCMF():
    global t, maxw, mincost, dis, flow, edge, last, s
    while spfa():
        # print("spfa 1")
        uuu = t
        maxw += flow[t]
        mincost += dis[t] * flow[t]
        while uuu != s:
            # print("spfa2")
            edge[last[uuu]].w -= flow[t]
            edge[last[uuu]^1].w += flow[t]
            uuu = pre[uuu]

shop = [[0 for col in range(55)] for row in range(55)]
ware = [[0 for col2 in range(55)] for row2 in range(55)]
cost = [[[0 for depth3 in range(55)] for col3 in range(55)] for row3 in range(55)]
rela = [[0 for col4 in range(2)] for row4 in range(55)]


line_count = 0
def process_input(in_str):
    global line_count
    line_count += 1
    s = in_str.split(" ")
    out_int = []
    for e in s:
        try:
            ee = int(float(e))
            out_int.append(ee)
        except ValueError:
            # print("Oh no")
            nokhod_siah = 0
    # print(f"line count no {line_count} str is {in_str} out is {out_int}")
    return out_int

n, m, k = tuple(process_input(input()))
while not n == 0 and not m == 0 and not k == 0:
    print(n , m, k)
    ans = 0
    for i in range(1, n + 1):
        input_shop = list(process_input(input()))
        if not len(input_shop) == k:
            print("error here", i, k, input_shop)
        for j in range(1, k + 1):
            shop[i][j] = input_shop[j - 1]
            rela[j][0] += shop[i][j]
    # print(f"shop: {[ind, subset ]}")
    # print(f"rela: {rela}")
    for i in range(1, m + 1):
        input_ware = list(process_input(input()))
        if not len(input_ware) == k:
            print("error here", i, k, input_ware)
        for j in range(1, k + 1):
            ware[i][j] = input_ware[j - 1]
            rela[j][1] += ware[i][j]
    # print(f"ware: {shop}")
    # print(f"rela: {rela}")
    for i in range(1, k + 1):
        for j in range(1, n + 1):
            input_cost = list(process_input(input()))
            if not len(input_cost) == k:
                print("error here", i, k, input_cost)
            for z in range(1, m + 1):
                cost[i][j][z] = input_cost[z - 1]
    # print(f"cost: {shop}")
    f = 0
    for i in range(1, k + 1):
        if rela[i][0] > rela[i][1]:
            f = 1
    if f != 0:
        print(-1)
        continue
    for z in range(1, k + 1):
        intt()
        s = 0
        t = 201
        for i in range(1, n + 1):
            add(s, i, shop[i][z], 0)
        for i in range(1, m + 1):
            add(i + 50, t, ware[i][z], 0)
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                add(i, j + 50, infinity, cost[z][j][i])
        MCMF()
        if maxw < rela[z][0]:
            print(-1)
            break
        ans += mincost
    if f == 0:
        print(ans)
    something = input()
    # print("here!")
    n, m, k = tuple(process_input(input()))
    # print(f"n, m, k = {m, n, k}")
