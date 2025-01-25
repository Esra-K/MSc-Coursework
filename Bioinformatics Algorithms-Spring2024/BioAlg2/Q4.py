import numpy as np
import string


def prim_mst(W):
    num_nodes = len(W)
    # Initialize arrays to keep track of the minimum spanning tree
    parent = [None] * num_nodes
    key = [float('inf')] * num_nodes
    mst_set = [False] * num_nodes
    # Start with the first node as the root
    key[0] = 0
    parent[0] = -1
    for _ in range(num_nodes):
        u = min((key[i], i) for i in range(num_nodes) if not mst_set[i])[1]
        mst_set[u] = True

        for v in range(num_nodes):
            if W[u][v] < key[v] and not mst_set[v]:
                key[v] = W[u][v]
                parent[v] = u
    # Construct the minimum spanning tree as a list of edges
    mst_edges = []
    for i in range(1, num_nodes):
        mst_edges.append((parent[i], i, W[parent[i]][i]))
    return mst_edges

class Node:
    def __init__(self, name, parent=0):
        self.name = name
        self.parent = parent
        self.children = set()

# The two following functions convert numbers to excel style letters, e.g. 29 -> 'AC'.
# source:https://stackoverflow.com/a/48984697/7314234
def divmod_excel(n):
    a, b = divmod(n, 26)
    if b == 0:
        return a - 1, b + 26
    return a, b

def to_excel(num):
    chars = []
    while num > 0:
        num, d = divmod_excel(num)
        chars.append(string.ascii_uppercase[d - 1])
    return ''.join(reversed(chars))

N = int(input())
w = np.zeros((N, N), dtype=float)
for i in range(N):
    w[i] = np.array(list(map(float, input().split())), dtype=float)
mst = prim_mst(w)
# print(mst)

nodes = {}
for i in range(N):
    nodes[i] = Node(i)

for parentt, child, weight in mst:
    nodes[child].parent = parentt
    nodes[parentt].children.add(child)

dfs_stack = [nodes[0]]
path = []
while len(dfs_stack) > 0:
    current = dfs_stack.pop()
    path.append(current.name)
    for child in current.children:
        dfs_stack.append(nodes[child])

path.append(0)
# print(path)
print("Tour:",  " ".join(list(map(lambda x: to_excel(x + 1), path))))

cost = 0
for i in range(len(path) - 1):
    cost += w[path[i]][path[i + 1]]
print("Total Distance:", cost)
