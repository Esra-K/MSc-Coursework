class Trie:
    class Edge:
        def __init__(self, ancestor, descendant, letter):
            self.ancestor_node = ancestor
            self.descendant_node = descendant
            self.letter = letter

    class Node:
        def __init__(self):
            self.letter = None
            self.edges = []

    def __init__(self):
        self.root = self.Node()

def add_edge(ancestor, descendant, letter):
    new_edge = Trie.Edge(ancestor, descendant, letter)
    ancestor.edges.append(new_edge)
    return new_edge

def prefix_trie_matching(prefix, trie):
    letter = prefix[0]
    current_node2 = trie.root
    pointer = 0
    while True:
        if len(current_node2.edges) == 0:
            return True
        flag = False
        for edge in current_node2.edges:
            if edge.letter == letter:
                flag = True
                current_node2 = edge.descendant_node
                if pointer < len(prefix) - 1:
                    letter = prefix[pointer + 1]
                    pointer = pointer + 1
                break
        if not flag:
            return False


def trie_match(sequence, trie):
    indices = []
    for i in range(len(sequence) - 1):
        prefix = sequence[i:]
        found = prefix_trie_matching(prefix, trie)
        if found:
            indices.append(i)
    return indices

k = int(input())
sequence = input()
patterns  = []
for i in range(k):
    patterns.append(input())

# Insert nodes in trie
trie = Trie()
for pattern in patterns:
    current_node = trie.root
    for letter in pattern:
        for edge in current_node.edges:
            if edge.letter == letter:
                current_node = edge.descendant_node
                break
        else:
            new_node = trie.Node()
            add_edge(current_node, new_node, letter)
            current_node = new_node
indices = trie_match(sequence, trie)
indices.sort()
print(" ".join(list(map(str, indices))))