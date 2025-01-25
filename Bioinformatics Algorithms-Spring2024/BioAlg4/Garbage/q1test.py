# python3

import sys
import queue
import numpy as np
from copy import deepcopy

class PeptideSequencing:
    def __init__(self):
        massDict, aaDict = self.AminoAcidMassDict()
        spectralVector = self.readFromFile()
        peptide = self.findPeptide(spectralVector, massDict)
        print(peptide)
        f = open('result.txt', 'w')
        f.write(peptide)
        f.close()

    def AminoAcidMassDict(self):
        massTable = '''
X 4
Z 5
G 57
A 71
S 87
P 97
V 99
T 101
C 103
I 113
L 113
n 114
D 115
K 128
Q 128
E 129
M 131
H 137
F 147
R 156
Y 163
W 186'''
        mass = massTable.split()
        return {int(mass[i + 1]): mass[i] for i in range(0, len(mass), 2)}, {mass[i]: int(mass[i + 1]) for i in
                                                                             range(0, len(mass), 2)}

    def _input(self):
        data = sys.stdin.read().strip().split()
        spectralVector = list(map(int, data))
        spectralVector.insert(0, 0)
        return spectralVector

    def readFromFile(self):
        f = input()
        # for line in f:
        data = f.strip().split()
            # print(data)
        spectralVector = list(map(int, data))
        spectralVector.insert(0, 0)
        print(spectralVector)
        return spectralVector

    def findPeptide(self, spectralVector, massDict):
        l = len(spectralVector)
        adj = [[] for _ in range(l)]
        for i in range(l):
            for j in range(i, l):
                if j - i in massDict:
                    adj[i].append(j)

        # Bellman-Ford algorithm
        dist = [-np.inf] * l
        parent = [None] * l
        dist[0] = 0
        updated = True
        for i in range(l - 1):
            if not updated:
                break
            updated = False
            for u in range(l):
                for v in adj[u]:
                    if dist[u] + spectralVector[v] > dist[v]:
                        dist[v] = dist[u] + spectralVector[v]
                        parent[v] = u
                        updated = True
        u = l - 1
        path = [u]
        while 0 != u:
            u = parent[u]
            path.insert(0, u)

        peptide = ''.join([massDict[path[i + 1] - path[i]] for i in range(len(path) - 1)])
        return peptide


if __name__ == "__main__":
    PeptideSequencing()