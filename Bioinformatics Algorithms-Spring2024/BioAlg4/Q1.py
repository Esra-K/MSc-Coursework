from collections import defaultdict
import math

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


def solve(vec):
    global residue2mass
    vec = [0] + vec
    mass2residue = {v: k for k, v in residue2mass.items()}
    # make dag
    dag = defaultdict(list)
    for i in range(len(vec)):
        for j in range(i + 1, len(vec)):
            if j - i in mass2residue:
                dag[i].append({"number": j, "weight": vec[j]})

    source_nodes = set(list(dag.keys()))
    dest_nodes = set([next_node["number"] for next_nodes in dag.values() for next_node in next_nodes])
    all_nodes = source_nodes.union(dest_nodes)

    dist = {node: -1 * math.inf for node in all_nodes}
    dist[0] = 0
    backward_paths = {0: []}
    for i in range(len(all_nodes) - 1):
        for u, vs in dag.items():
            for v in vs:
                if dist[u] + v["weight"] > dist[v["number"]]:
                    dist[v["number"]] = dist[u] + v["weight"]
                    backward_paths[v["number"]] = backward_paths[u] + [v["number"]]

    peptide = [mass2residue[j - i] for i, j in
               zip([0] + backward_paths[len(vec) - 1], backward_paths[len(vec) - 1])]
    print("".join(peptide))


spectrumv = list(map(int, input().strip().split()))
try:
    solve(spectrumv)
except: # KeyError
    residue2mass["X"] = 4
    residue2mass["Z"] = 5
    solve(spectrumv)
