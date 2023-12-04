from node import setup_tree, repetition_step, postprocessing_step, print_tree
import paths
import algorithms
import time
import random
import matplotlib.pyplot as plt

MAX_DEGREE = 5

def initialization(n: int):
    root = setup_tree(n, MAX_DEGREE)

    repetition_step(root)
    postprocessing_step(root)

    # Print the tree structure
    # print_tree(root)
    return root

def runtime_test():
    n_values = list(range(1, 202, 50))
    naive_runtimes = []
    fc_runtimes = []
    for n in n_values:
        naive_runtime, fc_runtime = get_runtime(n)
        naive_runtimes.append(naive_runtime)
        fc_runtimes.append(fc_runtime)
    plt.plot(n_values, naive_runtimes, marker='o', linestyle='-', label='Function 1')
    plt.plot(n_values, fc_runtimes, marker='o', linestyle='-', label='Function 2')

    plt.title('Runtime Comparison of Function 1 and Function 2')
    plt.xlabel('n')
    plt.ylabel('Runtime (seconds)')
    plt.legend()
    plt.grid(True)
    plt.show()

def get_runtime(n: int):
    naive_total_time = 0
    fc_total_time = 0
    for _ in range(n):
        naive_time, fc_time = query(n)
        naive_total_time += naive_time
        fc_total_time += fc_time
    naive_avg_time = naive_total_time / n
    fc_avg_time = fc_total_time / n
    return naive_avg_time, fc_avg_time

def query(n: int):
    target = random.randint(1, n**2)
    root = initialization(n)
    # path = paths.root_to_leaf_path(root)
    path = paths.leaf_node_leaf_path(root, n)
    naive_start_time = time.time()
    naive_res = algorithms.naive_algorithm(path, target)
    naive_end_time = time.time()
    fc_start_time = time.time()
    fc_res = algorithms.fractional_cascading(path, target)
    fc_end_time = time.time()
    naive_time = naive_end_time - naive_start_time
    fc_time = fc_end_time - fc_start_time
    is_correct = correctness_check(naive_res, fc_res)
    print(is_correct)
    # print(paths.print_path(path))
    # print(naive_res)
    # print(fc_res)
    print(naive_time, fc_time)
    return naive_time, fc_time

def correctness_check(list1, list2):
    result = all(elem1 == elem2 for elem1, elem2 in zip(list1, list2))
    return result

# runtime_test()
query(12)