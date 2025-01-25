# import time
import pandas as pd
import json
from unidecode import unidecode
import string
from nltk.corpus import stopwords
# from nltk.stem import SnowballStemmer, LancasterStemmer, WordNetLemmatizer
import krovetzstemmer
from collections import defaultdict, OrderedDict

import numpy as np
# from sklearn.preprocessing import normalize
# from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import pickle

def english_chinese(name):
    chinese = ""
    english = ""
    display_friendly = ""
    words = name.replace("/", " ").split(" ")
    if len(words) < 3:
        english = words[0]
        display_friendly = words[0]
        if len(words) > 1:
            chinese = words[1]
    else:
        english = "".join(words[:2]).strip()
        chinese = "".join(words[2:]).strip()
        display_friendly = " ".join(words[:2]).strip()
    english = unidecode(english).lower()
    return english, {english: unidecode(display_friendly)}, chinese


stemmer = krovetzstemmer.Stemmer()
# lemmatizer = WordNetLemmatizer()
ngram_relations = defaultdict(int)
frequencies = defaultdict(int)
def process_string(s, window_size=10, ngram_max_n=3):
    global ngram_relations, frequencies, english_names, stemmer  #, start_time
    temp = unidecode(s)
    temp = temp.lower()
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    temp = temp.translate(translator)
    templ = [word for word in temp.split() if not word in stopwords.words("english")]
    templ_c = []
    i = 0
    while i < len(templ) - 1:
        possible_fullname = templ[i] + templ[i + 1]
        if possible_fullname in english_names:
            templ_c.append(possible_fullname)
            i += 2
        else:
            templ_c.append(templ[i])
            i += 1
    templ = templ_c
    text_length = len(templ)
    for i in range(text_length):
        for j in range(1, ngram_max_n + 1):
            current_ngram = " ".join(templ[i: i + j]).strip()
            frequencies[current_ngram] += 1
            for distance in range(1, window_size):
                if i + distance < text_length:
                    for k in range(1, ngram_max_n + 1):
                        if i + distance + k <= text_length:
                            adjacent_ngram = " ".join(templ[i + distance: i + distance + k]).strip()
                            if current_ngram != adjacent_ngram:
                                ngram_relations[frozenset([current_ngram, adjacent_ngram])] += 1
        # if i % 1000 == 0:
        #     print(i, "time = ", time.time() - start_time)
    return True

with open('../Data/Sanguo Yanyi.json') as f_in:
    story = json.load(f_in)
story = {k:v for k, v in story.items() if k in ["Chapter " + str(i) for i in range(1, 121)]}
characters = pd.read_excel("../Data/SanguoYanyiChars.xlsx")
english_names, display_friendly_names, chinese_names = zip(*characters["Name"].map(english_chinese))
english_names = list(set(english_names))
display_friendly_names = {k: v for d in display_friendly_names for k, v in d.items()}

# start_time = time.time()
for chapter, content in story.items():
    title = content["title"]
    text = content["text"]
    a = process_string(title)
    b = process_string(text)

vals = list(frequencies.values())
vals.sort()
minn = 10 # vals[int(len(vals) * 0.05)]

def filter_good_frequencies(ngramset):
    global frequencies, vals, minn
    for word in ngramset:
        if frequencies[word] <= minn:
            return False
    return True


ngram_relations = {k: v for k, v in ngram_relations.items() if filter_good_frequencies(k)}
names = [name for name in english_names if frequencies[name] > minn * 5]

feature_words = set()
name_set = set(names)
for k, v in ngram_relations.items():
    if v > 10:
        print(frozenset(map(lambda key: display_friendly_names[key] if key in display_friendly_names.keys() else key, list(k))), v)
    if len(k.intersection(name_set)) > 0:
        for word in k:
            feature_words.add(word)
print("Length of the Feature Vector for each Word", len(feature_words))
feature_words = list(feature_words)

with open('../Data/ngram_relations.json', 'wb') as fp:
    pickle.dump(ngram_relations, fp, protocol=pickle.HIGHEST_PROTOCOL)

with open('../Data/display_friendly_names.json', 'wb') as fp:
    pickle.dump(display_friendly_names, fp, protocol=pickle.HIGHEST_PROTOCOL)

colors = []
texts = []
vecs = np.zeros((len(names), len(feature_words)))

degree = {name:0 for name in names}
for k, v in ngram_relations.items():
    kp = list(k)
    if kp[0] in names and kp[1] in names:
        degree[kp[0]] += 1
        degree[kp[1]] += 1
print("Num of Related People for Each Person:", degree)

names_indices_to_keep = []
for i, name in enumerate(names):
    texts.append(display_friendly_names[name])
    for j in range(len(feature_words)):
        if name == feature_words[j]:
            vecs[i][j] = 1000
        elif frozenset([name, feature_words[j]]) in ngram_relations.keys():
            vecs[i][j] = ngram_relations[frozenset([name, feature_words[j]])]
    if degree[name] > 5:
        names_indices_to_keep.append(i)

# vecs = normalize(vecs, axis=0, norm="l1")
vecs = vecs[names_indices_to_keep, :]
names = [names[i] for i in names_indices_to_keep]
texts = [texts[i] for i in names_indices_to_keep]

with open("../Data/vecs.txt", 'wb') as f:
    pickle.dump(vecs, f)
with open("../Data/names.txt", 'wb') as f:
    pickle.dump(names, f)

# pca = PCA(n_components=2)
# reduced = pca.fit_transform(vecs)
tsne = TSNE(n_components=2, random_state=42)
reduced = tsne.fit_transform(vecs)
t = reduced.transpose()
# tprim = t
selected_indices = [i for i in range(len(t[0]))] # if t[0][i] < 250 and t[1][i] > -100 and t[1][i] < 100]
tprim = t[:, selected_indices]
names = [names[i] for i in selected_indices]
texts = [texts[i] for i in selected_indices]
plt.scatter(tprim[0], tprim[1], s=[frequencies[name]/5 for name in names])
for i, txt in enumerate(texts):
    plt.annotate(txt, (tprim[0][i], tprim[1][i]))
plt.show()
