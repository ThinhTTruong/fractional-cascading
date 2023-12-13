import random
import time
from collections import deque

# Get the current time in seconds since the epoch as an integer
current_time = int(time.time())

# Set the seed for the random module based on the current time
random.seed(current_time)

#input values
INPUT_SIZE = 1
INPUT_DEGREE = 1

MAX_NODE_VALUE = 100
MAX_NODE_DEGREE = INPUT_DEGREE    #d
MAX_LIST_LENGTH = INPUT_SIZE    #max length of C(v)
INSERT_PROBABILITY = 1 / (2 * MAX_NODE_DEGREE)

# values for node list and augmented list
MIN_NUMBER_IN_LIST = 1
MAX_NUMBER_IN_LIST = INPUT_SIZE**2
MIN_BOUNDARY = MIN_NUMBER_IN_LIST - 1
MAX_BOUNDARY = MAX_NUMBER_IN_LIST + 1

class TreeNode:
    def __init__(self, value, max_list_len: int):
        self.value = value
        self.parent : TreeNode = None
        self.children : list[TreeNode] = []
        self.node_list = sorted([random.randint(MIN_NUMBER_IN_LIST, MAX_NUMBER_IN_LIST) for _ in range(random.randint(1, random.randint(1, max_list_len)))])
        self.augmented_list= [ListNode(MIN_BOUNDARY, self)] + [ListNode(MAX_BOUNDARY, self)]     #initialize the list with boundary values

        # set prev/next pointers for augmented_list
        for i in range(len(self.augmented_list)):
            if i > 0:
                self.augmented_list[i].set_prev(self.augmented_list[i-1])
            if i < len(self.augmented_list) - 1:
                self.augmented_list[i].set_next(self.augmented_list[i+1])

    def add_child(self, child_node: "TreeNode"):
        self.children.append(child_node)

    # generate augmented list without having proper pointer set
    def generate_augmented_list(self):
        # connect boundaries by bridges to neighbors
        for child in self.children:
            self.augmented_list[0].add_bridges(child.augmented_list[0])
            child.augmented_list[0].add_bridges(self.augmented_list[0])
            self.augmented_list[-1].add_bridges(child.augmented_list[-1])
            child.augmented_list[-1].add_bridges(self.augmented_list[-1])
        if self.parent:
            self.augmented_list[0].add_bridges(self.parent.augmented_list[0])        
            self.parent.augmented_list[0].add_bridges(self.augmented_list[0])   
            self.augmented_list[-1].add_bridges(self.parent.augmented_list[-1])
            self.parent.augmented_list[-1].add_bridges(self.augmented_list[-1])
        # perform insert on neighbors
        for value in self.node_list:
            list_node = insert_own_list(self.augmented_list, value, self)
            if list_node != None:
                insert_recursive(list_node, self)

    def post_processing(self):
        # set proper pointers
        start, end = 0, 0
        for i in range(len(self.augmented_list)):
            if self.augmented_list[i].tree_node:
                end = i
                current_proper = self.augmented_list[i]

                while start <= end:
                    self.augmented_list[start].set_proper(i, current_proper)
                    start += 1

        # add boundary values on node_list for naive algorithm
        self.node_list.insert(0, MIN_BOUNDARY)
        self.node_list.append(MAX_BOUNDARY)

    def print_augmented_list(self):
        values = list(map(lambda node: node.value, self.augmented_list))
        return values

class ListNode:
    def __init__(self, value, tree_node: TreeNode = None):
        self.value = value
        self.tree_node = tree_node
        self.bridges : list["ListNode"] = []
        self.prev = None
        self.next = None
        self.proper = None
    
    def add_bridges(self, list_node: "ListNode"):
        self.bridges.append(list_node)

    def set_prev(self, list_node: "ListNode"):
        self.prev = list_node

    def set_next(self, list_node: "ListNode"):
        self.next = list_node
    
    # Save proper as (index, list_node)
    def set_proper(self, index: int, list_node: "ListNode"):
        self.proper = (index, list_node)

def insert_own_list(augmented_list: list[ListNode], value: int, tree_node: TreeNode) -> ListNode:
    for i in range(len(augmented_list) - 1):
        if augmented_list[i].value < value <= augmented_list[i + 1].value:
            x, y = augmented_list[i], augmented_list[i + 1]

            if value == y.value:
                y.tree_node = tree_node
                return None
            else:
                new_node = ListNode(value, tree_node)
                # insert new node
                augmented_list.insert(i + 1, new_node)
                # uppdate pointers
                x.set_next(new_node)
                new_node.set_prev(x)
                new_node.set_next(y)
                y.set_prev(new_node)
                return new_node

def insert(tree_node: TreeNode, list_node: ListNode) -> ListNode:
    augmented_list = tree_node.augmented_list
    for i in range(len(augmented_list) - 1):
        if augmented_list[i].value < list_node.value <= augmented_list[i + 1].value:
            x, y = augmented_list[i], augmented_list[i + 1]
            
            if list_node.value == y.value:
                list_node.add_bridges(y)
                y.add_bridges(list_node)
                break
            else:
                # probability to run insert
                probability = random.uniform(0,1)
                if probability <= INSERT_PROBABILITY:
                    new_node = ListNode(list_node.value)
                    # insert new node
                    augmented_list.insert(i + 1, new_node)
                    # uppdate pointers
                    x.set_next(new_node)
                    new_node.set_prev(x)
                    new_node.set_next(y)
                    y.set_prev(new_node)
                    # add bridges
                    list_node.add_bridges(new_node)
                    new_node.add_bridges(list_node)
                    return new_node
    return None


def insert_recursive(list_node: ListNode, tree_node: TreeNode):
    stack = deque()
    if tree_node.parent:
        stack.append([tree_node.parent, list_node])
    if tree_node.children:
        for child in tree_node.children:
            stack.append([child, list_node])

    while stack:
        current_tree_node, current_list_node = stack.pop()

        if current_tree_node:
            new_list_node = insert(current_tree_node, current_list_node)
            if new_list_node:
                if current_tree_node.parent:
                    stack.append([current_tree_node.parent, new_list_node])
                if current_tree_node.children:
                    for child in current_tree_node.children:
                        stack.append([child, new_list_node])


# Create a random balanced tree with given size and max_degree
def create_whole_tree(size: int, max_degree: int):
    root = setup_tree(size, max_degree)
    repetition_step(root)
    postprocessing_step(root)
    return root

def setup_tree(size: int, max_degree: int):
    global INPUT_SIZE, INPUT_DEGREE
    INPUT_SIZE = size
    INPUT_DEGREE = max_degree
    update_variables()
    root = create_tree(size)
    return root

# Update global variables based on input
def update_variables():
    global MAX_NODE_DEGREE, MAX_LIST_LENGTH, INSERT_PROBABILITY, MAX_NUMBER_IN_LIST, MIN_BOUNDARY, MAX_BOUNDARY
    MAX_NODE_DEGREE = INPUT_DEGREE
    MAX_LIST_LENGTH = INPUT_SIZE
    INSERT_PROBABILITY = 1 / (2 * MAX_NODE_DEGREE)
    MAX_NUMBER_IN_LIST = INPUT_SIZE**2
    MIN_BOUNDARY = MIN_NUMBER_IN_LIST - 1
    MAX_BOUNDARY = MAX_NUMBER_IN_LIST + 1

# Helper to create a random balanced tree
def create_tree(height):
    if height <= 0:
        return None

    root = TreeNode(random.randint(1, MAX_NODE_VALUE), MAX_LIST_LENGTH)
    stack = deque([(root, height)])

    num_children = MAX_NODE_DEGREE - 1

    while stack:
        current_node, current_height = stack.pop()

        if current_height > 1:
            for _ in range(num_children):
                child = TreeNode(random.randint(1, MAX_NODE_VALUE), MAX_LIST_LENGTH)
                current_node.add_child(child)
                child.parent = current_node
                stack.append((child, current_height - 1))

    return root

# Process tree
def repetition_step(root: TreeNode):
    stack = [root]

    while stack:
        current_node = stack.pop()
        current_node.generate_augmented_list()

        stack.extend(current_node.children)

def postprocessing_step(root: TreeNode):
    stack = [root]

    while stack:
        current_node = stack.pop()
        current_node.post_processing()

        stack.extend(current_node.children)

# Print tree
def print_tree(root: TreeNode, level=0):
    if root is not None:
        print("  " * level + str(root.value), root.node_list, root.print_augmented_list())
        for child in root.children:
            print_tree(child, level + 1)