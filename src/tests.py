from node import create_tree, repetition_step, postprocessing_step, print_tree
import paths
import algorithms

TREE_HEIGHT = 2

def initialization():
    root = create_tree(TREE_HEIGHT)

    repetition_step(root)
    postprocessing_step(root)

    # Print the tree structure
    print_tree(root)
    return root

def algorithm_test():
    root = initialization()
    path = paths.root_to_leaf_path(root)
    naive_res = algorithms.naive_algorithm(path, 5)
    print(paths.print_path(path))
    print(naive_res)
    fc_res = algorithms.fractional_cascading(path, 5)
    print(fc_res)
    return naive_res

initialization()