class Trie:
    def __init__(self):
        self.all_nodes = []
        self.all_edges = []
        self.root = self.add_node()

    class node:
        def __init__(self):
            self.label = None
            self.edges = []

    class edge:
        def __init__(self):
            self.from_node = None
            self.target_node = None
            self.label = None

    def add_node(self):
        newNode = Trie.node()
        newNode.label = len(self.all_nodes)
        self.all_nodes.append(newNode)
        return newNode

    def add_edge(self, from_node, target_node, lbl):
        newEdge = Trie.edge()
        newEdge.from_node = from_node
        newEdge.target_node = target_node
        newEdge.label = lbl
        from_node.edges.append(newEdge)
        self.all_edges.append(newEdge)
        return newEdge


# def trie_construction(pattern_list):
#     trie = Trie()
#     for pattern in pattern_list:
#         current = trie.root
#         for x in pattern:
#             for edge in current.edges:
#                 if edge.letter == x:
#                     current = edge.target_node
#                     break
#             else:
#                 new_node = trie.add_node()
#                 trie.add_edge(current, new_node, x)
#                 current = new_node
#     return trie


def prefix_trie_matching(prefix, trie):
    symbol = prefix[0]
    node = trie.root
    idx = 1
    while True:
        if len(node.edges) == 0:
            return True
        found = False
        for edge in node.edges:
            if edge.label == symbol:
                found = True
                node = edge.target_node
                if idx < len(prefix):
                    symbol = prefix[idx]
                    idx += 1
                break

        if not found:
            return -1


def trie_matching(text, trie):
    result = []
    for i in range(len(text)):
        match = prefix_trie_matching(text[i:], trie)
        if match != -1:
            result.append(i)
    return result

k = int(input())
sequence = input()
patterns  = []
for i in range(k):
    patterns.append(input())

trie = Trie()
for pattern in patterns:
    current = trie.root
    for x in pattern:
        for edge in current.edges:
            if edge.label == x:
                current = edge.target_node
                break
        else:
            new_node = trie.add_node()
            trie.add_edge(current, new_node, x)
            current = new_node
result = trie_matching(sequence, trie)
print(' '.join(str(x) for x in result))