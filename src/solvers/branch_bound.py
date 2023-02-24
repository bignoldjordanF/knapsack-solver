from knapsack import KnapsackInstance, KnapsackAllocation
from collections import deque
from dataclasses import dataclass


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


def bound(u, n, capacity, items):
    if u.weight >= capacity:
        return 0
    
    profit_bound: int = u.value
    j: int = u.level + 1
    totweight: int = u.weight

    while j < n and totweight + items[j][1].weight <= capacity:
        totweight += items[j][1].weight
        profit_bound += items[j][1].value
        j += 1

    if j < n:
        profit_bound += (capacity - totweight) * items[j][1].value / items[j][1].weight
    
    return profit_bound


def branch_and_bound_solver(knapsack: KnapsackInstance) -> KnapsackAllocation:
    candidates: list = [(pid, cand) for pid, cand in enumerate(knapsack.items)]
    items: list = sorted(candidates, key=lambda t: t[1].value/t[1].weight, reverse=True)
    total_items = len(candidates)
    weight = knapsack.capacity

    Q: deque = deque()
    u: KnapsackNode = KnapsackNode(-1, 0, 0, 0, [])
    Q.append(u)

    maxProfit: int = 0
    maxAllocation: list = []
    while Q:
        u = Q.popleft()
        v = KnapsackNode(0, 0, 0, 0, [])
        if u.level == -1:
            v.level = 0

        if u.level == total_items - 1:
            continue

        v.level = u.level + 1
        v.weight = u.weight + items[v.level][1].weight
        v.value = u.value + items[v.level][1].value
        v.allocation = u.allocation[:] + [items[v.level][0]]

        if (v.weight <= weight and v.value > maxProfit):
            maxProfit = v.value
            maxAllocation = v.allocation

        v.bound = bound(v, total_items, weight, items)
        if (v.bound > maxProfit):
            Q.append(v)

        v = KnapsackNode(0, 0, 0, 0, []) 
        v.level = u.level + 1   
        v.weight = u.weight
        v.value = u.value
        v.allocation = u.allocation[:]
        v.bound = bound(v, total_items, weight, items)
        if (v.bound > maxProfit):
            Q.append(v)
        
    return KnapsackAllocation(maxAllocation, maxProfit)