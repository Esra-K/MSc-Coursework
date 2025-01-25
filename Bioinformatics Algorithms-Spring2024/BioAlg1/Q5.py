from collections import deque
class TrieNode:
    def __init__(self, label):
        self.label = label
        self.children = {}
        self.is_root = True

def build_trie(somestr):
    root = TrieNode("")
    for i in range(len(somestr)):
        current = root
        for j in range(i, len(somestr)):
            if somestr[j] not in current.children:
                current.children[somestr[j]] = TrieNode(somestr[j])
            current.is_root = False
            current = current.children[somestr[j]]
    return root

def merge_nodes(rootnode):
    nodes = [rootnode]
    while len(nodes) > 0:
        current_node = nodes.pop()
        while len(list(current_node.children.items())) == 1:
            child = list(current_node.children.values())[0]
            current_node.label = current_node.label + child.label
            current_node.children = child.children
        for child in current_node.children.values():
            nodes.append(child)
    return rootnode

def get_trie_nodes(rootnode):
    nodes = []
    q = deque()
    q.append(rootnode)
    while len(q) > 0:
        current_node = q.popleft()
        if len(current_node.label) > 0:
            nodes += [current_node.label]
        for child in current_node.children.values():
            q.append(child)
    return nodes


s = input()
trie = build_trie(s)
trie = merge_nodes(trie)
print("\n".join(sorted(get_trie_nodes(trie))))
