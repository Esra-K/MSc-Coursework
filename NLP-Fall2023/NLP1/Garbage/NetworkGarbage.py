import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import networkx as nx
import community
import pickle


with open("../Data/ngram_relations.json", 'rb') as file:
    ngram_relations = pickle.load(file)

with open("../Data/display_friendly_names.json", 'rb') as file:
     display_friendly_names = pickle.load(file)

node_chars = list(display_friendly_names.keys())

edges_tuples = []
for k, v in ngram_relations.items():
    kl = list(k)
    if kl[0] in node_chars and kl[1] in node_chars:
        edges_tuples.append((kl[0], kl[1], v/100))

# Create the graph
G = nx.Graph()

#Add the nodes
G.add_nodes_from(node_chars)

# Add the edges
G.add_weighted_edges_from(edges_tuples)

# Detect the communities of the graph
# partition = community.best_partition(G)

# Set the community partition as an attribute of the nodes of the graph
# nx.set_node_attributes(G, partition, 'group')
# nx.write_gexf(G, outfile)

# inputfile = ''

figfile_centr = 'centr.png'
figfile_distr = 'distr.png'
# G = nx.read_gexf(inputfile)

def calc_centralities(graph):
    dgc = nx.degree_centrality(graph)
    dgc = pd.DataFrame.from_dict(dgc, orient='index', columns=["DGC"])
    btc = nx.betweenness_centrality(graph)
    btc = pd.DataFrame.from_dict(btc, orient='index', columns=["BTC"])
    evc = nx.eigenvector_centrality(graph, weight='weight')
    evc = pd.DataFrame.from_dict(evc, orient='index', columns=["EVC"])

    df = pd.concat([dgc, btc, evc], axis=1)

    return df


df = calc_centralities(G)

def plot_centrality(centr, df, title, n, col_list):
    ax = plt.subplot(1, 3, n)
    s = df.sort_values(centr, ascending=False)[:10]
    x = list(s[centr].index)[::-1]
    y = list(s[centr])[::-1]

    for i, v in enumerate(y):
        bars = plt.barh(x[i], v, color=col_list[n - 1])

    plt.title(title, size=22)
    ax.get_xaxis().set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', length=0, labelsize=14)
print("123")

col_list = ["peachpuff", "plum", "orange"]
fig, ax = plt.subplots(1, 3, figsize=(15, 10))
plot_centrality("DGC", df, 'Degree Centrality', 1, col_list)
plot_centrality("BTC", df, 'Betweeness Centrality', 2, col_list)
plot_centrality("EVC", df, 'Eigenvector Centrality', 3, col_list)

plt.savefig(figfile_centr, dpi=300)

fig, ax = plt.subplots(figsize=(15, 10))

edge_df = nx.to_pandas_edgelist(G)
s = edge_df["weight"] * 100

ax = sns.displot(s)
plt.savefig(figfile_distr, dpi=300)