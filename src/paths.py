import random

from node import TreeNode

# path 1
def root_to_leaf_path(root: TreeNode, node_degree: int):
    if not root:
        return []
    
    path = []
    current = root

    while current:
        path.append(current)

        if not current.children:
            break

        child_index = random.randint(0, node_degree - 2)
        current = current.children[child_index]

    return path

def get_leaf_nodes(root: TreeNode):
    leaf_nodes: list[TreeNode] = []

    def dfs(node: TreeNode):
        if not node:
            return
        if not node.children:
            leaf_nodes.append(node)
        for child in node.children:
            dfs(child)

    dfs(root)
    return leaf_nodes

# path 2
def leaf_node_leaf_path(root: TreeNode, height: int):
    leaf_nodes = get_leaf_nodes(root)

    if not leaf_nodes:
        return []
    
    # Select a random starting leaf node
    start_leaf = random.choice(leaf_nodes)

    path = []
    current = start_leaf
    path.append(current)

    mid_point = height//2

    # Path going up
    for _ in range(mid_point):
        if current.parent:
            current = current.parent
            path.append(current)

    # Path going down
    for _ in range(mid_point):
        if current.children:
            current = random.choice(current.children)
            path.append(current)

    return path

# path 3
def up_and_down_path(root: TreeNode, node_degree: int, repetition_time: int):
    path = root_to_leaf_path(root, node_degree)
    new_path = []

    for node in path:
        new_path.append(node)

    for node in reversed(path[:-1]):
        new_path.append(node)
    for i in range(repetition_time -1):
        for node in path[1:]:
            new_path.append(node)

        for node in reversed(path[:-1]):
            new_path.append(node)
    return new_path