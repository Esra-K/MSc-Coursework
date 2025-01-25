from collections import defaultdict
import math
import time

def solve(specv, residue2mass):
    specv = [0] + specv
    print(specv)
    # make the graph (dag)
    dag = defaultdict(list)
    mass2residue = {v: k for k, v in residue2mass.items()}
    for i in range(len(specv)):
        for j in range(i + 1, len(specv)):
            if j - i in mass2residue:
                dag[i].append({"node": j, "weight": specv[j]})
    print(dag)
    # bellman-ford for longest path in dag
    set1 = set(list(dag.keys()))
    set2 = set([dic["node"] for dest in dag.values() for dic in dest])
    allnodes = set1.union(set2)
    dist = {node: -1000000000 for node in allnodes}
    dist[0] = 0
    parents = {}
    parents[0] = []
    for i in range(len(allnodes) - 1):
        for u, vs in dag.items():
            for v in vs:
                if dist[u] + v["weight"] > dist[v["node"]]:
                    dist[v["node"]] = dist[u] + v["weight"]
                    parents[v["node"]] = parents[u] + parents[v["node"]]
    print("parents", parents)
    time.sleep(1)
    # make peptide from parents[last_element]
    path = parents[len(specv) - 1]
    protseq = [mass2residue[j - i] for i, j in zip([0] + path, path)]
    print("".join(protseq))
    return 0


spectrumv = list(map(int, input().strip().split(" ")))
residue2mass = {
    "G": 57,
    "A": 71,
    "S": 87,
    "P": 97,
    "V": 99,
    "T": 101,
    "C": 103,
    "I": 113,
    "L": 113,
    "n": 114,
    "D": 115,
    "K": 128,
    "Q": 128,
    "E": 129,
    "M": 131,
    "H": 137,
    "F": 147,
    "R": 156,
    "Y": 163,
    "W": 186
}

try:
    solve(spectrumv, residue2mass)

except:
    residue2mass["X"] = 4
    residue2mass["Z"] = 5
    solve(spectrumv, residue2mass)