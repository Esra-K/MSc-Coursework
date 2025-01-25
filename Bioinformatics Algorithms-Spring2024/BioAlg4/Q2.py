from random import randint, choices
from copy import deepcopy

# Source: https://github.com/nutstick/rosalind/blob/master/ba2g.py

def make_rand_motifs(seqlist, k):
    motifs = []
    for seq in seqlist:
        index = randint(0, len(seq) - k)
        motifs.append(seq[index:index + k])
    return motifs

def make_profile(motifs, k):
    profile = [{ 'A': 1, 'C': 1, 'G': 1, 'T': 1}] * k
    for i in range(k):
        for j in range(len(motifs)):
            profile[i][motifs[j][i]] += 1
    return profile

def calc_motif_probs(profile, seq, k):
    probs = []
    for i in range(len(seq) - k + 1):
        probabil = 1
        for j in range(k):
            probabil *= (profile[j][seq[i + j]])
        probs.append(probabil)
    return probs

def score(motifs, k, t):
    profile = make_profile(motifs, k)
    sc = 0
    for a in range(len(profile)):
        sc += (4 + t - profile[a][max(profile[a], key=profile[a].get)])
    return sc

def gibbs(seqlist, k, t, n):
    new = make_rand_motifs(seqlist, k)
    old = deepcopy(new)
    for i in range(n):
        ind = randint(0, t - 1)
        del new[ind]
        profile = make_profile(new, k)
        probs = calc_motif_probs(profile, seqlist[ind], k)
        index = choices(list(range(0, len(seqlist[ind]) - k + 1)), probs)
        new.insert(ind, seqlist[ind][index[0]:index[0] + k])

        if score(new, k, t) < score(old, k, t):
            old = list(new)
    return old


k, t, n = tuple(map(int, input().strip().split(" ")))
# seq_list = list(input().strip().split())
seq_list = []
for i in range(t):
  seq_list.append(input().strip())

old_motifs = gibbs(seq_list, k, t, n)
for i in range(20):
    new_motifs = gibbs(seq_list, k, t, n)
    if score(new_motifs, k, t) < score(old_motifs, k, t):
        old_motifs = new_motifs

for motif in old_motifs:
    print(motif)