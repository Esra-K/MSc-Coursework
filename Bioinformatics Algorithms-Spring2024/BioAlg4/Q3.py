# Install and import required packages
import random
import numpy as np
import pandas as pd
from collections import Counter, defaultdict

motif_len = 6
random_alignment_total = 200
iteration = 200


# Load dataset file
with open("example.fasta") as fasta:
  sequences = [x.strip("\n") for i, x in enumerate(fasta.readlines()) if i%2==1]
print(sequences[0])

# Prepare data
# Centralizes all relevant and reusable data, encompassing a comprehensive range of information. This includes the concatenation of all bases into a single string, a tally of individual base counts, an inventory of contiguous motifs, and the calculation of cumulative sums.
a = defaultdict(int)
def rec_dd():
  return defaultdict(rec_dd)
d = rec_dd()
for s in sequences:
  for i in range(len(s) - motif_len + 1):
    if d[s][s[i:i+motif_len]] != "y":
      a[s[i:i + motif_len]] += 1
      d[s][s[i:i + motif_len]] = "y"


for k, v in sorted(a.items(), key=lambda j:j[1], reverse=True):
  print(k, v)