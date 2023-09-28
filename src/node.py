import random

MAX_NUMBER_IN_LIST = 1000
MAX_NODE_VALUE = 100
MAX_NODE_DEGREE = 10    #d
MAX_LIST_LENGTH = 10    #max length of C(v)

# values for node list and augmented list
MIN_NUMBER_IN_LIST = 1
MAX_NUMBER_IN_LIST = 1000
MIN_BOUNDARY = MIN_NUMBER_IN_LIST - 1
MAX_BOUNDARY = MAX_NUMBER_IN_LIST + 1


class TreeNode:
    def __init__(self, value, max_list_len):
        self.value = value
        self.children = []
        self.node_list = sorted([random.randint(MIN_NUMBER_IN_LIST, MAX_NUMBER_IN_LIST) for _ in range(random.randint(1, random.randint(1, max_list_len)))])
        self.augmented_list= [ListNode(MIN_BOUNDARY, False)] + [ListNode(value, True) for value in self.node_list] + [ListNode(MAX_BOUNDARY, False)]     #initialize the list with elements from node_list and boundary values

    def add_child(self, child_node):
        self.children.append(child_node)

    def generate_augmented_list(self):
        # connect boundaries by bridges to neighbors
        for child in self.children:
            self.augmented_list[0].add_bridges(child.augmented_list[0])
            self.augmented_list[-1].add_bridges(child.augmented_list[-1])


    def print_augmented_list(self):
        values = map(lambda node: node.value, self.augmented_list)
        return list(values)


class ListNode:
    def __init__(self, value, is_in_node_list):
        self.value = value
        self.is_in_node_list = is_in_node_list
        self.bridges = []
        self.pred = None
        self.next = None
        self.proper = None
    
    def add_bridges(self, list_node):
        self.bridges.append(list_node)

    def set_pred(self, list_node):
        self.pred = list_node

    def set_next(self, list_node):
        self.next = list_node
    
    def set_proper(self, list_node):
        self.proper = list_node

# Create a random balanced tree
def create_random_tree(max_depth, current_depth):
    if current_depth > max_depth:
        return None

    root = TreeNode(random.randint(1, MAX_NODE_VALUE), MAX_LIST_LENGTH)
    num_children = random.randint(0, MAX_NODE_DEGREE - 1)
    for _ in range(num_children):
        child = create_random_tree(max_depth, current_depth + 1)
        if child is not None:
            root.add_child(child)

    return root

# Print tree
def print_tree(root, level=0):
    if root is not None:
        print("  " * level + str(root.value), root.node_list, root.print_augmented_list())
        for child in root.children:
            print_tree(child, level + 1)



# Example usage:
max_depth = 3  # Maximum depth of the tree
root = create_random_tree(max_depth, 1)

# Print the tree structure along with the sorted numbers in each node
print_tree(root)