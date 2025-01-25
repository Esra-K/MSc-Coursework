n = int(input())
kmers = []
for i in range(n):
    kmers.append(input().strip())

debruyne = []
for kmer in kmers:
    debruyne.append((kmer[:-1], kmer[1:]))
    reverse_kmer = kmer.translate(str.maketrans(
        {"A":"T", "C": "G", "G":"C", "T":"A"}))[::-1]
    debruyne.append((reverse_kmer[:-1], reverse_kmer[1:]))
for x, y in sorted(set(debruyne)):
    print("(" + x + " , " + y + ")")
