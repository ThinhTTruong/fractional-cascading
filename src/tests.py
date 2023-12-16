from node import create_whole_tree
import paths
import algorithms
import time
import random
import matplotlib.pyplot as plt
import math

REPETITION_TIME = 10000

def initialization(n: int, max_degree: int):
    root = create_whole_tree(n, max_degree)

    return root

def query(n: int, max_degree: int, path_option: int):
    target = random.randint(1, n**2)
    root = initialization(n, max_degree)
    if path_option == 1:
        path = paths.root_to_leaf_path(root, max_degree)
    elif path_option == 2:
        path = paths.leaf_node_leaf_path(root, n)
    else:
        path = paths.up_and_down_path(root, max_degree, REPETITION_TIME)
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
    return naive_time, fc_time

def correctness_check(list1, list2):
    result = all(elem1 == elem2 for elem1, elem2 in zip(list1, list2))
    return result

def get_runtime(n: int, max_degree: int, path_option: int):
    naive_total_time = 0
    fc_total_time = 0
    for _ in range(n):
        naive_time, fc_time = query(n, max_degree, path_option)
        naive_total_time += naive_time
        fc_total_time += fc_time
    naive_avg_time = naive_total_time / n
    fc_avg_time = fc_total_time / n
    return naive_avg_time, fc_avg_time

def runtime_test(max_degree: int, max_n: int, path_option: int):
    n_values = list(range(1, max_n+1, 2))
    naive_runtimes = []
    fc_runtimes = []
    for n in n_values:
        naive_runtime, fc_runtime = get_runtime(n, max_degree, path_option)
        naive_runtimes.append(naive_runtime)
        fc_runtimes.append(fc_runtime)
    plt.plot(n_values, naive_runtimes, marker='o', linestyle='-', label='Naive')
    plt.plot(n_values, fc_runtimes, marker='o', linestyle='-', label='Fractional Cascading')

    plt.title('Runtime Comparison of Naive and Fractional Cascading Algorithm')
    plt.xticks(range(min(n_values), math.ceil(max(n_values))+1, 2))
    plt.xlabel('n')
    plt.ylabel('Runtime (seconds)')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    runtime_test(max_degree=3, max_n=9, path_option=3)

if __name__ == "__main__":
    main()