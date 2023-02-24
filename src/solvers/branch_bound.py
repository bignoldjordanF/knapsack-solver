from knapsack import KnapsackInstance, KnapsackAllocation
from dataclasses import dataclass
from collections import deque

# References:
# [0] https://www.geeksforgeeks.org/implementation-of-0-1-knapsack-using-branch-and-bound/?ref=lbp
# [1] https://stackoverflow.com/questions/43965835/knapsack-branch-and-bound-wrong-result

@dataclass
class KnapsackNode:
    level: int
    value: int
    bound: int
    weight: int
    allocation: list


def bound(node: KnapsackNode, n_items: int, capacity: int, items: list):
    if node.weight >= capacity:
        return 0
    
    value_bound: int = node.value
    level: int = node.level + 1
    weight: int = node.weight

    while level < n_items and weight + items[level][1].weight <= capacity:
        weight += items[level][1].weight
        value_bound += items[level][1].value
        level += 1
    
    if level < n_items:
        value_bound += (capacity - weight) * \
            items[level][1].value / items[level][1].weight
    
    return value_bound


def branch_and_bound_solver(knapsack: KnapsackInstance) -> KnapsackAllocation:
    items: list = [(pid, cand) for pid, cand in enumerate(knapsack.items)]
    items: list = sorted(items, key=lambda i: i[1].value/i[1].weight, reverse=True)

    queue: deque = deque()
    queue.append(KnapsackNode(-1, 0, 0, 0, []))

    max_value: int = 0
    max_allocation: list = []

    while queue:
        curr: KnapsackNode = queue.popleft()
        child: KnapsackNode = KnapsackNode(0, 0, 0, 0, [])

        if curr.level == -1:
            child.level = 0
        
        if curr.level == len(items) - 1:
            continue

        child.level = curr.level + 1
        child.weight = curr.weight + items[child.level][1].weight
        child.value = curr.value + items[child.level][1].value
        child.allocation = curr.allocation[:] + [items[child.level][0]]
        child.bound = bound(child, len(items), knapsack.capacity, items)

        if child.weight <= knapsack.capacity and child.value > max_value:
            max_value = child.value
            max_allocation = child.allocation
        
        if child.bound > max_value:
            queue.append(child)

        child = KnapsackNode(0, 0, 0, 0, [])
        child.level = curr.level + 1
        child.weight = curr.weight
        child.value = curr.value
        child.allocation = curr.allocation[:]
        child.bound = bound(child, len(items), knapsack.capacity, items)

        if child.bound > max_value:
            queue.append(child)
    
    return KnapsackAllocation(max_allocation, max_value)

