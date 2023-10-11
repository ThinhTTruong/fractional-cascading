import random

from node import TreeNode, MAX_NODE_DEGREE

def root_to_leaf_path(root: TreeNode):
    if not root:
        return []
    
    path = []
    current = root

    while current:
        path.append(current)

        if not current.children:
            break

        child_index = random.randint(0, MAX_NODE_DEGREE - 2)
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

def leaf_node_leaf_path(root: TreeNode, height: int):
    leaf_nodes = get_leaf_nodes(root)

    if not leaf_nodes:
        return []
    
    # Select a random starting leaf node
    start_leaf = random.choice(leaf_nodes)

    path = []
    current = start_leaf
    path.append(current)

    # Path going up
    for _ in range(height - 1):
        current = current.parent
        path.append(current)

    # Path going down
    for _ in range(height - 1):
        current = random.choice(current.children)
        path.append(current)

    return path