from Bio.Align.Applications import ClustalwCommandline
from Bio import AlignIO
from difflib import SequenceMatcher
import numpy as np


def similar(a, b):
    # source: https://stackoverflow.com/a/53538659
    return SequenceMatcher(None, a, b).ratio()


i = int(input("Enter a number from 1 to 5 (file No):"))
infile = f"BioAlg-HW2-2/input{i}.txt"
clustalw2_path = "clustalw2.exe"
clustalw_cline = ClustalwCommandline(clustalw2_path, infile=infile)
stdout, stderr = clustalw_cline()
aln = infile.replace(".txt", ".aln")
align = AlignIO.read(aln, "clustal")
align_list = align.__str__().split("\n")[1:]
dict_align = {s.split()[1]: s.split()[0] for s in align_list}
# print(dict_align)

sim_dict = {}
seqs = list(dict_align.keys())
nseq = len(seqs)
sim_matrix = np.zeros((nseq, nseq), dtype=float)
for i in range(nseq):
    for j in range(i):
        sim_matrix[i][j] = similar(dict_align[seqs[i]], dict_align[seqs[j]])
        sim_matrix[j][i] = sim_matrix[i][j]
# print(sim_matrix)
sim_scores = {seqs[i]: np.mean(sim_matrix[i]) for i in range(nseq)}
print(min(sim_scores, key=sim_scores.get))
