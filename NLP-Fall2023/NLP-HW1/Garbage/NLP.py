import time
import nltk
from nltk.stem import SnowballStemmer, WordNetLemmatizer
# nltk.download('wordnet')
from nltk.corpus import stopwords
# nltk.download('stopwords')
import pandas as pd
import json
from unidecode import unidecode
from collections import defaultdict, OrderedDict
import string

import gensim
# from gensim.models import Word2Vec

import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


frequencies = defaultdict(int)
title_frequency_weight = 1
def tokenize(s, is_title=False):
    global frequencies, title_frequency_weight
    temp = unidecode(s)
    temp = temp.lower()
    # map punctuation to space
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
    # stemmer = SnowballStemmer(language='english')
    # lemmatizer = WordNetLemmatizer()
    # templ = [stemmer.stem(word) for word in templ]
    for word in templ:
        frequencies[word] += 1 * (title_frequency_weight if is_title else 1)
    return templ


def english_chinese(name):
    chinese = ""
    english = ""
    display_friendly = ""
    words = name.split(" ")
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


def js_read(filename: str):
    with open(filename) as f_in:
        return json.load(f_in)


story = js_read('../Data/Sanguo Yanyi.json')
story = {k:v for k, v in story.items() if k in ["Chapter " + str(i) for i in range(1, 121)]}
characters = pd.read_excel("../Data/SanguoYanyiChars.xlsx")
english_names, display_friendly_names, chinese_names = zip(*characters["Name"].map(english_chinese))
english_names = list(set(english_names))
display_friendly_names = {k: v for d in display_friendly_names for k, v in d.items()}

tokenized = {}
for chapter, content in story.items():
    title = content["title"]
    text = content["text"]
    tokenized[chapter] = tokenize(title, is_title=True) + tokenize(text)

num_of_features = 50
w2v = gensim.models.Word2Vec([chapter for chapter in tokenized.values()], min_count = 10,
                                                vector_size = num_of_features, window = 50)
frequencies = OrderedDict(sorted(frequencies.items(), key=lambda v: v, reverse=True))

indices = {}
colors = []
names = [name for name in english_names if name in w2v.wv.key_to_index.keys() and frequencies[name] > 100]
vecs = np.zeros((len(names), num_of_features))

for i, name in enumerate(names):
    indices[i] = display_friendly_names[name]
    vecs[i] = w2v.wv[name]

# pca = PCA(n_components=2)
# reduced = pca.fit_transform(vecs)
tsne = TSNE(n_components=2, random_state=42)
reduced = tsne.fit_transform(vecs)
t = reduced.transpose()
plt.scatter(t[0], t[1], s=[frequencies[name]/5 for name in names])
for i, txt in indices.items():
    plt.annotate(txt, (t[0][i], t[1][i]))
plt.show()
