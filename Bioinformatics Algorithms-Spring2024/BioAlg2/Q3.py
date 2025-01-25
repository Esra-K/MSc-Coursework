from collections import defaultdict
# import random
# https://cs.stackexchange.com/questions/44274/simple-example-2-approximation-for-vertex-cover

V, E = map(int, input().split())
edges = []
for i in range(E):
    v1, v2 = map(int, input().split())
    edges.append((v1, v2))

adjacency_dict = defaultdict(list)
for edge in edges:
    adjacency_dict[edge[0]].append(edge[1])
    adjacency_dict[edge[1]].append(edge[0])

vert_cover = set()
while len(edges) > 0:
    v = max(adjacency_dict.items(), key=lambda x: len(x[1]))[0]
    # u = random.choice(adjacency_dict[v])
    u = max({key: adjacency_dict[key] for key in adjacency_dict[v]}.items(), key=lambda x: len(x[1]))[0]
    vert_cover.add(v)
    if len(adjacency_dict[u]) > 1:
        vert_cover.add(u)
    for key, val in adjacency_dict.items():
        adjacency_dict[key] = [vertex for vertex in val if not vertex in [u, v]]
    del adjacency_dict[v]
    del adjacency_dict[u]
    edges = list(filter(lambda x: (not x[0] in [u, v]) and (not x[1] in [u, v]), edges))

print(" ".join(list(map(str, list(vert_cover)))))
