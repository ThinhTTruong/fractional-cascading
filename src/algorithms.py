from node import TreeNode, ListNode

def naive_algorithm(path: list[TreeNode], target: int):
    result = []
    for tree_node in path:
        # binary seach
        search_result = binary_search_naive(tree_node.node_list, target)
        result.append(search_result)
    return result

def binary_search_naive(lst, target):
    left, right = 0, len(lst) - 1

    while left < right:
        mid = (left + right) // 2

        if lst[mid] == target:
            return target
        elif lst[mid] < target:
            left = mid + 1
        else:
            right = mid

    return lst[right] 

def fractional_cascading(path: list[TreeNode], target: int):
    result = []

    # Binary search on first tree node
    current_node = path[0]
    (first_index, first_value) = binary_search_fc(current_node.augmented_list, target)
    if first_value == target and current_node.augmented_list[first_index].tree_node:
        result.append(first_value)
    else:
        result.append(current_node.augmented_list[first_index].proper[1].value)

    cur_index = first_index
    # fractional cascading on other nodes
    for i in range(len(path)-1):
        cur_index, res = helper(cur_index, path[i], path[i+1], target)
        result.append(res)
        # print('trying')

    return result

def binary_search_fc(lst: list[ListNode], target: int):
    #return (index, value)
    left, right = 0, len(lst) - 1

    while left < right:
        mid = (left + right) // 2

        if lst[mid].value == target:
            return (mid, target)
        elif lst[mid].value < target:
            left = mid + 1
        else:
            right = mid 
    return (right, lst[right].value)

def helper(cur_index: int, cur_node: TreeNode, next_node: TreeNode, target: int):
    cur_list = cur_node.augmented_list
    current = cur_list[cur_index]
    found = False
    value = 0
    while current:
        if current.bridges:
            for bridge in current.bridges:
                if bridge.tree_node == next_node: #step 2
                    current = bridge #step 3
                    found = True
                    break
        if found:
            break
        else:
            current = current.next
    value = current.proper[1].value
    while current and current.prev.value >= target: #step 4
        current = current.prev
        if current.proper:
            value = current.proper[1].value
    
    index = next_node.augmented_list.index(current)

    if current.proper and value == target:
        return (index, target) # return index of current element in A(v), and matching value in C(v)

    return (index, value) # return index of element in A(v), and smallest value in C(v) that is greater target

