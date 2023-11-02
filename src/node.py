import random
import time

# Get the current time in seconds since the epoch as an integer
current_time = int(time.time())

# Set the seed for the random module based on the current time
random.seed(current_time)


MAX_NODE_VALUE = 100
MAX_NODE_DEGREE = 3    #d
MAX_LIST_LENGTH = 1    #max length of C(v)
# INSERT_PROBABILITY = 1 / (2 * MAX_NODE_DEGREE)
INSERT_PROBABILITY = 1

# values for node list and augmented list
MIN_NUMBER_IN_LIST = 1
MAX_NUMBER_IN_LIST = 10
MIN_BOUNDARY = MIN_NUMBER_IN_LIST - 1
MAX_BOUNDARY = MAX_NUMBER_IN_LIST + 1


class TreeNode:
    def __init__(self, value, max_list_len: int):
        self.value = value
        self.parent : TreeNode = None
        self.children : list[TreeNode] = []
        self.node_list = sorted([random.randint(MIN_NUMBER_IN_LIST, MAX_NUMBER_IN_LIST) for _ in range(random.randint(1, random.randint(1, max_list_len)))])
        self.augmented_list= [ListNode(MIN_BOUNDARY, self)] + [ListNode(value, self) for value in self.node_list] + [ListNode(MAX_BOUNDARY, self)]     #initialize the list with elements from node_list and boundary values

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
        for list_node in self.augmented_list[1: -1]:
            insert_recursive(list_node, self)

    # set proper pointers
    def post_processing(self):
        start, end = 0, 0
        for i in range(len(self.augmented_list)):
            if self.augmented_list[i].value != MIN_BOUNDARY and self.augmented_list[i].value != MAX_BOUNDARY and self.augmented_list[i].tree_node:
                end = i
                current_proper = self.augmented_list[i]

                while start <= end:
                    self.augmented_list[start].set_proper(i, current_proper)
                    start += 1

    def print_augmented_list(self):
        values = list(map(lambda node: node.value, self.augmented_list))
        return values

    def print_augmented_list2(self):
        values = list(map(lambda node: node.print_pointers(), self.augmented_list))
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

    def print_pointers(self):
        return list(map(lambda node: node.value, self.bridges)), list(map(lambda node: node.tree_node.value if node.tree_node else node.value, self.bridges)), self.prev.value if self.prev else self.prev, self.next.value if self.next else self.next, self.proper[1].value if self.proper else self.proper

def insert(augmented_list: list[ListNode], list_node: ListNode) -> bool:
    for i in range(len(augmented_list) - 1):
        if augmented_list[i].value < list_node.value <= augmented_list[i + 1].value:
            x, y = augmented_list[i], augmented_list[i + 1]
            
            if list_node.value == y.value:
                list_node.add_bridges(y)
                y.add_bridges(list_node)
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
                    return True
    return False

def insert_recursive(list_node: ListNode, tree_node: TreeNode):
    # perform insert on neighbors
    insert_parent = False
    if tree_node.parent:
        insert_parent = insert(tree_node.parent.augmented_list, list_node)
    if tree_node.children:
        for child in tree_node.children:
            insert_child = insert(child.augmented_list, list_node)
            if insert_child:
                insert_recursive(list_node, child)
    if insert_parent:
        insert_recursive(list_node, tree_node.parent)

# Create a random balanced tree
def create_tree(height: int, parent: TreeNode = None):
    if height <= 0:
        return None

    root = TreeNode(random.randint(1, MAX_NODE_VALUE), MAX_LIST_LENGTH)
    root.parent = parent
    num_children = MAX_NODE_DEGREE - 1

    for _ in range(num_children):
        child = create_tree(height-1, root)
        if child is not None:
            root.add_child(child)

    return root

# Process tree
def repetition_step(root: TreeNode):
    root.generate_augmented_list()

    for child in root.children:
        repetition_step(child)

def postprocessing_step(root: TreeNode):
    root.post_processing()

    for child in root.children:
        postprocessing_step(child)

# Print tree
def print_tree(root: TreeNode, level=0):
    if root is not None:
        print("  " * level + str(root.value), root.node_list, root.print_augmented_list())
        print(root.print_augmented_list2())
        print
        for child in root.children:
            print_tree(child, level + 1)