import pickle
import networkx as nx

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

g = nx.Graph()
g.add_nodes_from(node_chars)
g.add_weighted_edges_from(edges_tuples)
nx.write_gexf(g, "../Data/charnetwork.gexf")
