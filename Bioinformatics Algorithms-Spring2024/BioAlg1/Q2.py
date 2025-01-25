from collections import deque

maxn = int(5e2+10)
infinity = int(0x3f3f3f3f)
# n = 0
# f = 0
# d = 0
f1 = 0
d1 = 0
x = 0

G = [[0 for j in range(maxn)] for i in range(maxn)]
pre = [0 for i in range(maxn)]
flow = [0 for i in range(maxn)]

def bfs(s, t):
    global pre, flow, G
    q = deque()
    pre = [-1 for i in range(maxn)]
    flow = [0 for i in range(maxn)]
    pre[s] = 0
    flow[s] = infinity
    q.append(s)
    while len(q) > 0:
        val = q[0]
        q.popleft()
        if val == t:
            break
        for i in range(1, t + 1):
            if pre[i] == -1 and G[val][i] != 0 and i != s:
                pre[i] = val
                flow[i] = min(flow[val], G[val][i])
                q.append(i)
    if pre[t] == -1:
        return -1
    else:
        return flow[t]

def ek(s, t):
    tol = 0
    data = 0
    while True:
        data = bfs(s, t)
        if data == -1:
            break
        pp = t
        while pp != s:
            G[pre[pp]][pp] -= data
            G[pp][pre[pp]] += data
            pp = pre[pp]
        tol += data
    return tol

n, f, d = tuple(map(int, input().split(" ")))
G = [[0 for j in range(maxn)] for i in range(maxn)]
for i in range(1, f + 1):
    G[0][i] = 1
for i in range(1, n + 1):
    G[f + 2 * i - 1][f + 2 * i] = 1
for i in range(f + 2 * n + 1, f + 2 * n + d + 1):
    G[i][f + 2 * n + d + 1] = 1
for i in range(1, n + 1):
    params = list(map(int, input().split(" ")))
    f1 = params[0]
    d1 = params[1]
    params = params[2:]
    temp = 0
    for j in range(1, f1 + 1):
        x = params[j - 1]
        G[x][f + 2 * i - 1] = 1
        temp += 1
    params = params[temp:]
    for j in range(1, d1 + 1):
        x = params[j - 1]
        G[f + 2 * i][f + 2 * n + x] = 1
print(ek(0, 2 * n + f + d + 1))