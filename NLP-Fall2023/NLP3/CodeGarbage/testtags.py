from collections import defaultdict, Counter
import re

tags = []
with open("../Data/Taglist.txt") as file:
    for line in file:
        tags.append(line.rstrip())

tagcount = Counter(tags)

clean_tags = {k: v for k, v in tagcount.items() if k+">name" in tagcount.keys()} # and k+">description" in tagcount.keys()}
clean_with_kids = {k: v for k, v in tagcount.items() if re.match("(" + "|".join(clean_tags.keys()) + ")", k) }
for k, v in clean_with_kids.items():
    print(k, v)

print(sum(clean_with_kids.values()) / sum(tagcount.values()))
